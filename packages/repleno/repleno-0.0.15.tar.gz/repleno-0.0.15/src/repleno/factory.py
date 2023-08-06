from __future__ import annotations
from datetime import datetime
from repleno.utils import *

import warnings
import repleno as repl


class Factory:

    def __init__(self, bom=None, bom_mapping = None, parameters=None, parameters_mapping=None):
        self._skus = {}

        if bom:
            self.load_bom(bom, bom_mapping)

        if parameters:
            self.load_parameters(parameters, parameters_mapping)

        self._cache = {}  # don't use @lru_cache because of memory leak

    @property
    def all_item_location_pairs(self) -> set:
        return {key for key in self._skus.keys()}

    @property
    def all_skus(self) -> set:
        return {key for key in self._skus.values()}

    @property
    def all_items(self) -> set:
        # if no location available, return only item
        return {item_loc[0] for item_loc in self._skus.keys()}

    @property
    def abc_classifications(self) -> dict:
        result = {}
        for sku in self.skus:
            result[(sku.item, sku.location)] = sku.abc_classification

        return result

    def get_sku(self, item: str, location: str = None) -> repl.SKU:
        item_fmt = str(item).strip().upper()

        if not location:
            return self._skus.get((item_fmt, None))
        
        location_fmt = str(location).strip().upper()
        return self._skus.get((item_fmt, location_fmt))

    def load_bom(
        self,
        data: str | list[dict],
        mapping: list[dict] = None,
    ):
        """
        Load bill of materials into the model.
 
        Parameters
        ----------
        data : str | list[dict]
            A CSV filename or a list of dictionaries with the following
            keys/column names: 

            - "item": str,  --> mandatory
            - "child_item": str,  --> mandatory
            - "location": str, 
            - "child_location": str,
            - "qty": int | float.
            
        mapping : dict, optional
            Remap the keys or column names if data does not have the expected
            ones. Keys are the expected keys (above) and values are the new
            names in your dictionaries or columns.
            If mapping is specified, all keys/column names are considered
            mandatory and error is raised if they are not found.
            
        Raises
        ------
        ValueError
            If the data argument does not match the supported data types.
        

        Notes
        -----
        Leading zeros in CSV files
            If you saved the file using the UI, make sure to explicitly format
            your text columns as text. Otherwise the leading zeros will be
            removed and you might face problems like the below example:

            Example:
            In the CSV file, you have the following item: "000A1010". When you
            call `fact.get_sku("000A1010")`, you might not find it because when
            saving the file, the leading zeros were removed, and now you can
            only find this SKU with: `fact.get_sku("A1010")`.
            
        """

        mandatory_keys = ["item", "child_item"]
        optional_keys = ["location", "child_location", "qty"]
        data = extract_and_transform_data(data, mandatory_keys, optional_keys, mapping)

        if isinstance(data, list) and data:
            for record in data:
                try:
                    # Avoid raising exceptions when getting optional values with .get()
                    self._link_and_register_skus(
                        item = record["item"],
                        child_item = record["child_item"],
                        location = record.get("location", None),
                        child_location = record.get("child_location", None),
                        qty = record.get("qty", None),
                    )
                except KeyError:
                    print(f"Bad key/column name: make sure the following are in the file: {[key for key in mandatory_keys.keys()]}")
                    raise

            return

 
    def _link_and_register_skus(
        self,
        item,
        child_item,
        qty=1,
        location=None,
        child_location=None,
    ):

        # Format items and locations in the same way that SKU will do for
        # consistency when using get_sku()
        item = item.strip().upper()
        child_item = child_item.strip().upper()

        if location:
            location = location.strip().upper()

        if child_location:
            child_location = child_location.strip().upper()

        # Get or register SKUs in factory
        sku = self._skus.setdefault((item, location), repl.SKU(item=item, location=location))
        child_sku = self._skus.setdefault((child_item, child_location), repl.SKU(item=child_item, location=child_location))
        sku._link_child(child_sku, qty)


    def load_parameters(self, data: str | list, mapping: dict = None, sellable_true_value: str = None, phantom_true_value: str = None, obsolete_true_value: str = None) -> None:
        """
        Load parameters into the model.

        Parameters
        ----------
        data : str | list
            A CSV filename or a list of dictionaries with the following
            keys/column names:

            - "item": str,  --> mandatory
            - "location": str, 
            - "sellable": bool , 
            - "phantom": bool, 
            - "obsolete": bool, 
            - "status": str,
            - "abc_classification": str, 
            - "safety_stock_qty": int | float, 
            - "lead_time": int | float,
            - "inventory_qty": int | float, 
            - "minimum_order_qty"; int | float,
            - "batch_size": int | float 
            - "maximum_order_qty": int | float 
 
        mapping : dict, optional
            Remap the keys or column names if data does not have the expected
            ones. Keys are the expected keys (above) and values are the new
            names in your dictionaries or columns.
            If mapping is specified, all keys/column names are considered
            mandatory and error is raised if they are not found.

        sellable_true_value : str, optional
            The string value considered as true (e.g. "Yes", "Y"), by default
            None
            
        phantom_true_value : str, optional
            The string value considered as true (e.g. "Yes", "Y"), by default
            None

        obsolete_true_value : str, optional
            The string value considered as true (e.g. "Yes", "Y"), by default
            None

        """
        
        # the fields "sellable", "phantom" and obsolete must be booleans. 
        # If the input data is not boolean, the truth values can be defined by passing a string 
        # that represents the truth values to the parameters: `sellable_true_value` and `phantom_true_value`, correspondingly.
        # 

        mandatory_keys = ["item"]
        optional_keys = ["location", "sellable", "phantom", "obsolete", "status", "abc_classification", "safety_stock_qty", "lead_time", "inventory_qty", "minimum_order_qty", "batch_size", "maximum_order_qty"]
        data = extract_and_transform_data(data, mandatory_keys, optional_keys, mapping)

        if isinstance(data, list) and data:
            for record in data:
                try:
                    item_code = record["item"]
                    location = record.get("location", None)

                    sku = self.get_sku(item_code, location)
                    if sku is None:
                        warnings.warn(
                            f"SKU Not Found: {sku}",
                            UserWarning,
                            stacklevel=2,
                        )
                        continue
                    
                    sellable_data = record.get("sellable", None)
                    if sellable_data:
                        # Transform string to boolean if needed
                        if sellable_true_value:
                            sellable_data = True if sellable_data.strip() == sellable_true_value else False

                        sku.sellable = sellable_data

                    phantom_data = record.get("phantom", None)
                    if phantom_data:
                        # Transform string to boolean if needed
                        if phantom_true_value:
                            phantom_data = True if phantom_data.strip() == phantom_true_value else False

                        sku.phantom = phantom_data

                    obsolete_data = record.get("obsolete", None)
                    if obsolete_data:
                        # Transform string to boolean if needed
                        if obsolete_true_value:
                            obsolete_data = True if obsolete_data.strip() == obsolete_true_value else False

                        sku.obsolete = obsolete_data

                    status_data = record.get("status", None)
                    if status_data:
                        sku.status = status_data

                    abc_classification_data = record.get("abc_classification", None)
                    if abc_classification_data:
                        sku.abc_classification = abc_classification_data

                    safety_stock_qty_data = record.get("safety_stock_qty", None)
                    if safety_stock_qty_data:
                        sku.safety_stock_qty = safety_stock_qty_data

                    lead_time_data = record.get("lead_time", None)
                    if lead_time_data:
                        sku.lead_time = lead_time_data

                    inventory_qty_data = record.get("inventory_qty", None)
                    if inventory_qty_data:
                        sku.inventory_qty = inventory_qty_data
                    
                    minimum_order_qty_data = record.get("minimum_order_qty", None)
                    if minimum_order_qty_data:
                        sku.minimum_order_qty = minimum_order_qty_data

                    batch_size_data = record.get("batch_size", None)
                    if batch_size_data:
                        sku.batch_size = batch_size_data

                    maximum_order_qty_data = record.get("maximum_order_qty", None)
                    if maximum_order_qty_data:
                        sku.maximum_order_qty = maximum_order_qty_data

                except KeyError:
                    print(f"Bad key/column name: make sure the following are in the file: {[key for key in mandatory_keys.keys()]}")
                    raise

            return


    def _get_mps_orders(self, data, mapping=None, date_format="%Y-%m-%d"):
        """
        Load the master production schedule (MPS) in the model.

        Args:
            - data (Union[str, List[Dict]]): The input data, either a csv file
            with the below columns names or a list of dictionary with the below key names:
                1. "item_code"
                2. "due_date"
                3. "qty"
            In case the data does not have these columns, use the field_mapping
            parameter for mapping.
            - field_mapping (List[Dict[str, str]], optional): When the columns
            in the data are not the default ones. Defaults to an empty dictionary.
            e.g.:
                {
                    "item_code": "<field_name_in_data_with_parent_code>",
                    "due_date": "production_date"
                    "qty": "quantity"
                }

        Raises:
            ValueError: If the input data is invalid.

        Returns:
            None
        """
        mandatory_keys = ["item", "due_date", "qty"]
        data = extract_and_transform_data(data, mandatory_keys=mandatory_keys, mapping=mapping)

        output = []

        if isinstance(data, list):
            for i in data:
                item = self.get_sku(i["item"])

                if item is None:
                    warnings.warn(
                        f"No MRP ran for '{i['item']}', as no BOM found for it.",
                        UserWarning,
                        stacklevel=2,
                    )
                    continue

                try:
                    order = repl._Order(
                        item,
                        datetime.strptime(i["due_date"], date_format),
                        convert_to_float(i["qty"]),
                    )

                    output.append(order)

                except Exception as e:
                    print(f"Item code: '{i['item']}' raised the exception: {e}.\n")
                    raise

            return output

        raise ValueError(
            "Invalid argument. It must be a csv file path or a list of dictionaries."
        )

    def run_mrp(self, mps, date_format="%Y-%m-%d", mapping=None, output=""):
        """
        Breaks down the top level orders (MPS) into dependent orders for
        individual subassemblies, component parts and raw materials that are
        required to produce the top level orders.

        How does an MRP work (more specifically)?

        The process starts at the top level with the Master Productin Schedule (MPS).
        There are 3 distinct steps in preparing the MRP schedule:

        1. Exploding:
            Explosion uses the Bill of Materials (BOM). The first level is represented
            by the MPS and this is "exploded" down to components. With that, it provides
            how many components are needed to manufacture the items in the MPS.

        2. Netting:
            The next step is "netting", in which any inventory on hand is subtracted
            form the gross requirement determined through explosion.
            
        3. Offsetting:
            The final step determines when the manufacturing should start so that the
            finished items are available when required. To do so, the lead time will be
            subtracted from the dates and passed down on to the next components. 

        Parameters
        ----------
        mps : _type_
            _description_
        date_format : str, optional
            _description_, by default "%Y-%m-%d"
        mapping : _type_, optional
            _description_, by default None
        output : str, optional
            _description_, by default ""

        Returns
        -------
        _type_
            _description_

        Note
        ----
        Calling this function alters the Factory object state (inventories will
        be decreased or increased depending on the requirements generated by the
        MPS.)
        
        """
        
        mps_orders = self._get_mps_orders(mps, mapping, date_format)
        if not mps_orders:
            return []

        purchased_orders = []
        for order in mps_orders:
            exploded_order = self._explode_orders(order)
            purchased_orders += exploded_order

        purchased_orders = self._populate_order_type(purchased_orders)

        result = []
        for order in purchased_orders:
            result.append(order.to_dict())

        if output:
            to_csv(result, output, date_keys=["due_date"])
        else:
            return result


    def _explode_orders(self, top_order):
        # How it works?
        # It traverses the tree and for each stock unit iterates over its child
        # stock units. For each child stock unit, calculate the following:
        #
        # Scenarios                                             A   B   C
        # ----------------------------------------------------------------
        # current_inventory_qty                                     2   5   3
        # gross_order                                          -6  -3  -3
        # new_inventory_qty                                        -4   2   0
        # net_order (to replenish inventory_qty)                    4   -   -
        # net_order_rounded (according to lot size)             5   -   -
        # final_inventory_qty (net_order_rounded - gross_order)     1   -   -
        # ----------------------------------------------------------------

        # Depth-first traversal (DFS) is used because it's easier when
        # debugging. Because each branch is exploded at the time, so there's
        # less skip steps when debugging.
        # Pre-order traversal because root node should be visited and have its
        # calculations first, beforemoving to the child nodes.
        
        if not isinstance(top_order, repl._Order):
            raise AttributeError("work_orders must be instance of WorkOrder.")

        result = []
        stack = [top_order]
        while stack:
                # Get last order added on the queue and get the net of it
                current_order = stack.pop()
                sku = current_order.sku

                # ============ visit ============

                # reduce inventory


                # record requirement order, if needed, based on safety stock and inventory levels


                # check if purchase order should be created based on lot sizes

                # - static:
                #       - lot for lot (no lot size): as soon as inv < ss => release order
                #       - fixed-lot (reorder point): record date when inv<ss, from this date,
                #       keep adding requirements until it reaches the lot
                #       quantity and then release the order
                #       
                # - periodic:
                #       - period of supply: record date when inv<ss, from this date,
                #       get all requirements in the next X days specified by the
                #       user, then release the order
                #       
                # - dynamic: 
                # 

                # increase inventory accordingly if replenishment order 


                net_order = self._get_net_workorder(current_order)



                # adjust inventories acc. to new order
                qty_left_for_inventory = net_order.qty - current_order.qty
                sku.inventory_qty += qty_left_for_inventory

                # register order, if needed
                if net_order.qty == 0:
                    continue   
                result.append(net_order)

                # adjust the lead time
                current_order.due_date = remove_business_days(
                    current_order.due_date, sku.lead_time
                )
                # ========= end visit ==========

                for child_link in reversed(sku.child_links):
                    exploded_qty = net_order.qty * child_link.qty

                    stack.append(
                        repl._Order(child_link.sku, current_order.due_date, exploded_qty)
                    )

        return result



    def _get_net_workorder(self, order: repl._Order) -> repl._Order:
        """Subtracts the order qty from the inventory_qty balance for this
        stock unit and if inventory_qty falls below zero returns an order with the
        net requirements lot sized.

        """
        reorder_qty = (order.qty + order.sku.safety_stock_qty) - order.sku.inventory_qty

        if reorder_qty > 0:
            net_qty_rounded = order.sku._adjust_qty_to_moq_and_batch(reorder_qty)
            return repl._Order(order.sku, order.due_date, net_qty_rounded)
        else:
            return repl._Order(order.sku, order.due_date, 0)


    def _populate_order_type(self, orders: List[repl._Order]):
        """Populate the type property of Order instances """
        for order in orders:
            if order.sku._type == repl._SKUType.CHILD:
                order._type = repl._OrderType.PURCHASE_ORDER
            else:
                order._type = repl._OrderType.WORK_ORDER

        return orders


    def export_abc_classifications(self, csv_path):
        to_csv(
            self._format_abc_classification_for_csv(self.abc_classifications), csv_path
        )

    def _format_abc_classification_for_csv(self, data) -> List:
        headers = ["Item", "Classification"]
        output = [headers]

        for item, classification in data.items:
            output.append([item, classification])

        return output

    def _group_and_sort_item_quantities_by_date(self, required_orders, open_orders):
        required_orders_hashed = hash_dicts_list(required_orders)
        open_orders_hashed = hash_dicts_list(open_orders)

        if (required_orders_hashed, open_orders_hashed) in self._cache:
            return self._cache[(required_orders_hashed, open_orders_hashed)]

        # Convert dictionaries of Order objects
        required_orders_fmt = [
            repl._Order(
                repl.SKU(o["item_code"]),
                datetime.strptime(o["due_date"], "%Y-%m-%d").date(),
                o["qty"],
            )
            for o in required_orders
        ]
        open_orders_fmt = [
            repl._Order(
                repl.SKU(o["item_code"]),
                datetime.strptime(o["due_date"], "%Y-%m-%d").date(),
                o["qty"],
            )
            for o in open_orders
        ]

        # Use a dictionary to keep track of dates and quantities for each item_code.
        # The dictionary has item_code as the key, and its value is a list of all
        # orders (required + open) stored as tuples.
        # Each tuple contains order date and quantity
        quantities = {}

        for order in required_orders_fmt:
            item = order.sku.item
            date = order.due_date
            quantity = order.qty * (-1)
            if item not in quantities:
                quantities[item] = []
            quantities[item].append((date, quantity))

        for order in open_orders_fmt:
            item = order.sku.item
            date = order.due_date
            quantity = order.qty
            if item not in quantities:
                quantities[item] = []
            quantities[item].append((date, quantity))

        # For each item_code, sort the tuples by date in ascending order
        for item in quantities:
            quantities[item].sort(key=lambda x: x[0])

        self._cache[(required_orders_hashed, open_orders_hashed)] = quantities
        return quantities

    # todo: rename qty to quantity and adjust this as well all over the project
    def get_inventory_over_time(
        self,
        required_orders,
        open_orders,
        item_codes=[],
        shortages_only=False,
        required_orders_field_mapping={},
        open_orders_field_mapping={},
        to_csv_path=None,
    ):
        """
        Calculates the difference in quantities across time for each item_code in the
        required_orders and open_orders lists.

        Args:
            - required_orders (List[Dict[str, any]]): A list of dictionaries
            representing required orders.  Each dictionary contains the
            following keys: 'product', 'date' and 'quantity'.  This is usually
            the return value of the `run_mrp` method.

            - open_orders (List[Dict[str, any]]): A list of dictionaries
            representing open orders.  Each dictionary contains the following
            keys: 'product', 'date' and 'quantity'. The quantities here are
            always positive.

        Returns:
            - List[Dict[str, any]]: A list of dictionaries representing the
            difference in quantities across time.  Each dictionary contains the
            following keys: 'item_code', 'date_from', 'date_to', 'qty'.  If the 'to'
            key is None, it means that there are not other orders modifying the
            quantity anymore.
        """

        ro_field_mapping = {
            "item_code": required_orders_field_mapping.get("item_code", "item_code"),
            "due_date": required_orders_field_mapping.get("due_date", "due_date"),
            "qty": required_orders_field_mapping.get("qty", "qty"),
        }
        required_orders = extract_and_transform_data(required_orders, ro_field_mapping)

        oo_field_mapping = {
            "item_code": open_orders_field_mapping.get("item_code", "item_code"),
            "due_date": open_orders_field_mapping.get("due_date", "due_date"),
            "qty": open_orders_field_mapping.get("qty", "qty"),
        }
        open_orders = extract_and_transform_data(open_orders, oo_field_mapping)

        # Group all orders and organise them in following format: List({'item': (date, qty)})
        quantities = self._group_and_sort_item_quantities_by_date(
            required_orders, open_orders
        )

        # For each item, iterate through its tuples (date, qty)
        result = []
        for item in quantities:
            if item_codes and item not in item_codes:
                continue

            qty = 0
            prev_date = None
            for date, quantity in quantities[item]:
                if prev_date is None:  # for first tuple
                    qty += quantity
                    prev_date = date
                    continue

                if shortages_only and qty > 0:
                    qty += quantity
                    prev_date = date
                    continue

                record = {
                    "item_code": item,
                    "date_from": prev_date,
                    "date_to": date,
                    "qty": qty,
                }
                result.append(record)
                qty += quantity
                prev_date = date

            # For last tuple
            result.append(
                {
                    "item_code": item,
                    "date_from": prev_date,
                    "date_to": None,
                    "qty": qty,
                }
            )

        if to_csv_path is not None:
            result_fmt = self._format_inventory_qty_over_time_output_for_csv(result)
            to_csv(result_fmt, to_csv_path)
        else:
            return result

    def _format_inventory_qty_over_time_output_for_csv(self, data) -> List:
        headers = ["Item", "From", "To", "Quantity"]
        output = [headers]

        for d in data:
            item = d["item_code"]
            date_from = f"{d['date_from']:%Y-%m-%d}"
            date_to = f"{d['date_to']:%Y-%m-%d}" if d["date_to"] is not None else ""
            qty = d["qty"]

            output.append([item, date_from, date_to, qty])

        return output


    def get_collaterals(self, target, items_only=False, phaseouts=None, child_only=False): 
        sku = self.get_sku(target)

        phaseout_skus = set()
        for i in phaseouts:
            phaseout_skus.add(self.get_sku(i))

        return sku.get_collaterals(items_only=items_only, phaseout_skus=phaseout_skus, child_only=child_only)


def run():
    pass
