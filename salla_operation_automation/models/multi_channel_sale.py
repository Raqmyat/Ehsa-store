from logging import getLogger
import requests
from odoo import _, fields, models, api
from odoo.exceptions import UserError

_logger = getLogger(__name__)

class MultiChannelSale(models.Model):
    _inherit = 'multi.channel.sale'

    sync_order_status_cron = fields.Boolean(string="Enable Order Status Sync Cron")
    sync_inventory_global_cron = fields.Boolean(string="Enable Global Inventory Sync Cron")
    salla_branch_id = fields.Char(string="The default branch of Salla", store=True)

    def action_fetch_salla_branches(self):
        """A function to retrieve branches from a basket and display them to the user."""
        self.ensure_one()
        if not self.access_token:
            raise UserError("Please make sure you have the Access Token first!")

        url = "https://api.salla.dev/admin/v2/branches"
        headers = {"Authorization": f"Bearer {self.access_token}"}

        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                branches = response.json().get('data', [])
                for branch in branches:
                    _logger.info(f"Branch Name: {branch['name']} - ID: {branch['id']}")

                if branches:
                    self.salla_branch_id = str(branches[0]['id'])
                    return {
                        'effect': {
                            'fadeout': 'slow',
                            'message': f"The branches have been successfully acquired! The selected branch: {branches[0]['name']}",
                            'type': 'rainbow_man',
                        }
                    }
            else:
                raise UserError("Failure in the branches of the basket.")
        except Exception as e:
            raise UserError(f"An error occurred: {str(e)}")

    @api.model
    def _cron_action_fetch_salla_branches(self):
        """A Cron-specific function to search for salla channels and automatically fetch their branches"""
        channels = self.search([('channel', '=', 'salla'), ('state', '=', 'validate')])
        for channel in channels:
            try:
                _logger.info(f"Auto-fetching branches for channel: {channel.name}")
                channel.action_fetch_salla_branches()
            except Exception as e:
                _logger.error(f"Error auto-fetching branches for {channel.name}: {str(e)}")

    def open_salla_automation_cron_views(self):
        """Open your Crown settings directly"""
        cron_xml_id = self._context.get('cron_xml_id')
        cron_id = self.env.ref(f'salla_operation_automation.{cron_xml_id}', raise_if_not_found=False)
        return {
            'type': 'ir.actions.act_window',
            'name': 'Configure Cron',
            'res_model': 'ir.cron',
            'res_id': cron_id.id if cron_id else False,
            'view_mode': 'form',
            'target': 'new',
        }

    @api.model
    def action_sync_salla_orders_status(self):
        _logger.info("🚀 Starting to synchronize basket order statuses...")
        channels = self
        print("channels",channels)
        if not channels:
            channels = self.search([
                ('channel', '=', 'salla'),
                ('state', '=', 'validate')
            ])

        for channel in channels:
            if not channel.access_token:
                _logger.warning(f"No access token found for channel: {channel.name}")
                continue

            _logger.info(f"--- Start Syncing Salla Status: {channel.name} ---")
            headers = {"Authorization": f"Bearer {channel.access_token}"}

            order_mappings = self.env['channel.order.mappings'].search([
                ('channel_id', '=', channel.id),
                ('order_name.state', 'not in', ['done', 'cancel'])
            ], order='id desc', limit=200)

            for mapping in order_mappings:
                order = mapping.order_name
                url = f"https://api.salla.dev/admin/v2/orders/{mapping.store_order_id}"

                try:
                    response = requests.get(url, headers=headers, timeout=10)
                    if response.status_code == 200:
                        salla_data = response.json().get('data', {})
                        status_slug = salla_data.get('status', {}).get('slug')

                        mapping.write({'store_order_status': status_slug})

                        if status_slug in ['shipped', 'completed']:
                            self._do_force_validate_warehouse(order)

                        elif status_slug in ['in_progress','completed']:
                            self._do_force_post_invoice(order)
                            if order.state == 'sale':
                                order.action_done()

                        _logger.info("Status Slug",status_slug)
                        if status_slug in ['restored', 'restoring']:
                            _logger.info("🔄 Processing Return for Order: %s", order.name)
                            picking_success = self._handle_picking_return(order)
                            invoice_success = self._handle_invoice_return(order)

                            if picking_success and invoice_success:
                                order.write({'state': 'done'})

                        _logger.info(f"Success: {order.name} updated to {status_slug}")
                    else:
                        _logger.error(f"Salla API Error for {order.name}: {response.status_code}")

                except Exception as e:
                    _logger.error(f"Exception for {order.name}: {str(e)}")

    def _do_force_validate_warehouse(self, order):
        pickings = order.picking_ids.filtered(lambda p: p.state not in ('done', 'cancel'))
        for picking in pickings:
            try:
                if picking.state in ['confirmed', 'waiting', 'assigned']:
                    picking.action_assign()

                for move in picking.move_ids:
                    if move.state not in ('done', 'cancel'):
                        move.quantity = move.product_uom_qty

                picking.with_context(skip_backorder=True, skip_sms=True).button_validate()

                # self.env.cr.commit()
                print(f"📦The store has closed the order {order.name} Successfully")
            except Exception as e:
                print(f"❌Store authentication failed {order.name}: {str(e)}")

    def _do_force_post_invoice(self, order):
        invoices = order.invoice_ids.filtered(lambda i: i.state == 'draft')
        for inv in invoices:
            inv.action_post()

    def _handle_picking_return(self, order):
        """Create a warehouse return and invoice credit note - fixed duplication"""
        _logger.info(f"🔍 Start processing the return request: {order.name}")

        done_pickings = order.picking_ids.filtered(
            lambda p: p.state == 'done' and p.picking_type_code == 'outgoing'
        )

        for picking in done_pickings:
            already_returned = any(
                m.returned_move_ids.filtered(lambda rm: rm.state != 'cancel') for m in picking.move_ids)

            if already_returned:
                _logger.info(f"⏩ Skipped {picking.name} Because it was previously returnedً.")
                continue

            try:
                _logger.info(f"🛠️A warehouse return is being created for: {picking.name}")
                ctx = {
                    'active_id': picking.id,
                    'active_ids': [picking.id],
                    'active_model': 'stock.picking',
                }
                return_wizard = self.env['stock.return.picking'].with_context(ctx).create({})

                if not return_wizard.product_return_moves:
                    continue

                for line in return_wizard.product_return_moves:
                    line.quantity = line.move_id.quantity or line.move_id.product_uom_qty

                res_action = return_wizard.action_create_returns()
                return_picking_id = res_action.get('res_id')

                if return_picking_id:
                    return_picking = self.env['stock.picking'].browse(return_picking_id)
                    for move in return_picking.move_ids:
                        move.quantity = move.product_uom_qty

                    return_picking.with_context(skip_backorder=True).button_validate()
                    _logger.info(f"✅ The warehouse return was successfully approved: {return_picking.name}")
                    self.env.cr.commit()
            except Exception as e:
                _logger.error(f"❌ The warehouse return failed for {picking.name}: {str(e)}")
        return True

    def _handle_invoice_return(self, order):
        """Create credit note for posted invoices - Odoo 18 Compatible based on UI Debug"""

        posted_invoices = order.invoice_ids.filtered(
            lambda i: i.state == 'posted' and i.move_type == 'out_invoice'
        )

        if not posted_invoices:
            _logger.info(f"No posted invoices for order {order.name}")
            return True

        for inv in posted_invoices:
            existing_refund = self.env['account.move'].search([
                ('reversed_entry_id', '=', inv.id),
                ('move_type', '=', 'out_refund'),
                ('state', '!=', 'cancel'),
            ], limit=1)

            if existing_refund:
                _logger.info(f"Skipping invoice {inv.name}, credit note already exists: {existing_refund.name}")
                continue

            try:
                _logger.info(f"Creating credit note for invoice {inv.name}")

                ctx = {
                    'active_model': 'account.move',
                    'active_ids': inv.ids,
                    'active_id': inv.id,
                }


                wizard_vals = {
                    'reason': f'Return for Order {order.name}',
                    'journal_id': inv.journal_id.id,
                    'date': fields.Date.context_today(self),
                }

                wizard = self.env['account.move.reversal'].with_context(ctx).create(wizard_vals)
                print("wizard", wizard)

                wizard.refund_moves()

                credit_note = self.env['account.move'].search([
                    ('reversed_entry_id', '=', inv.id),
                    ('move_type', '=', 'out_refund'),
                    ('state', '=', 'draft')
                ], limit=1)

                if credit_note:
                    credit_note.action_post()
                    _logger.info(f"✅ Credit note created and posted: {credit_note.name}")
                    self.env.cr.commit()
                else:
                    _logger.warning(f"⚠️ Credit note created but not found in draft for {inv.name}")

            except Exception as e:
                _logger.error(f"❌ Error while creating credit note for {inv.name}: {str(e)}")
                return False

        return True


    @api.model
    def action_sync_all_inventory_to_salla(self):
        """Update the quantities of all linked products in Odoo to the Salla store"""
        channels = self.search([('channel', '=', 'salla'), ('state', '=', 'validate')])

        target_channels = self if (self and self._name == 'multi.channel.sale') else channels

        for channel in target_channels:
            if not channel.access_token:
                continue

            _logger.info(f"🚀 Inventory sync started for channel: {channel.name}")

            product_mappings = self.env['channel.product.mappings'].search([
                ('channel_id', '=', channel.id)
            ])

            for mapping in product_mappings:
                product = mapping.product_name
                if not product:
                    continue

                try:
                    current_qty = int(product.qty_available)

                    salla_variant_id = getattr(mapping, 'store_variant_id', mapping.store_product_id)
                    branch_id = channel.salla_branch_id
                    print("branch_id", branch_id)
                    if not branch_id:
                        branch_id = 1680270783
                    if not salla_variant_id:
                        continue

                    url = f"https://api.salla.dev/admin/v2/products/variants/{salla_variant_id}"
                    headers = {
                        "Authorization": f"Bearer {channel.access_token}",
                        "Content-Type": "application/json",
                    }


                    payload = {"quantities": [{"branch": int(branch_id), "quantity": current_qty}]}
                    response = requests.put(url, json=payload, headers=headers, timeout=15)

                    if response.status_code in [200, 201]:
                        _logger.info(f"✅ Product {product.name} updated to: {current_qty}")
                    else:
                        _logger.error(f"❌ Salla API Error: {response.status_code}")

                except Exception as e:
                    _logger.error(f"❌ Exception for product {product.name}: {str(e)}")
                    if "cursor already closed" in str(e):
                        break

        _logger.info("🏁 Global inventory sync operation finished.")
