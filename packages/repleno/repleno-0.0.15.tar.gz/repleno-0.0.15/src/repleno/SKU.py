from __future__ import annotations

from enum import Enum
from typing import List
from repleno.utils import *
import warnings
from collections import deque
import hashlib

import pptree
import repleno

class _OutputFormatter:
    """
    Makes things easier to store in a standard dictionary.
    """

    def __init__(self, max_stack_size=None):
        self.records = {}
        self._skus = set()
        self._highest_level = None
        self._max_stack_size = max_stack_size
        self._stack_size = 0
        self._collateral_side = None

    def store(self, sku, parent_skus, child_skus, direction, level=0):
        if not isinstance(sku, SKU):
            raise TypeError(f"sku must be an instance of Links, not of {type(sku)}")

        if isinstance(parent_skus, SKU):
            parent_skus = [parent_skus]

        if isinstance(child_skus, SKU):
            child_skus = [child_skus]

        self._skus.add(sku)

        # check stack size
        self._stack_size += 1
        if self._max_stack_size and self._stack_size > self._max_stack_size:
            raise BufferError("Stack size exceeded maximum stack size.")

        # create key if does not exist
        self.records.setdefault(
            sku,
            {
                "sku_level": 0,
                "parent_skus": set(),
                "child_skus": set(),
                "_iterations": 0
            },
        )

        # store the values
        if parent_skus:
            self.records[sku]["parent_skus"] = self.records[sku]["parent_skus"].union(
                parent_skus
            )

        if child_skus:
            self.records[sku]["child_skus"] = self.records[sku]["child_skus"].union(
                child_skus
            )

        self.records[sku]["_iterations"] = self.records[sku]["_iterations"] + 1

        self.records[sku]["sku_level"] = level

        # check level
        if self._highest_level is None or self._highest_level < level:
            self._highest_level = level

        if direction not in ["children", "parents"]:
            raise TypeError(f"direction must be one either 'children' or 'parents'")

        if direction == "children":
            if level < self.records[sku]["sku_level"]:
                self.records[sku]["sku_level"] = level

        if direction == "parents":
            if level > self.records[sku]["sku_level"]:
                self.records[sku]["sku_level"] = level

    def get_output(self, items_only=False, attributes=None, hash_keys=False):
        if items_only:
            skus = self.records.keys()
            return { sku.item if not sku.location else (sku.item, sku.location) for sku in skus}

        f_result = deque()
        sku_id_pairs = {}

        for sku, val in self.records.items():
            SKUing = str(sku.location) + str(sku.item)

            # Get or generate hash for all skus in this iteration
            # Why? Hash skus to avoid having special characters in ID
            sku_id_pairs.setdefault(
                sku, hashlib.sha256(SKUing.encode()).hexdigest()
            )
            sku_id = sku_id_pairs[sku]

            parent_ids = set()
            for p_sku in val["parent_skus"]:
                parent_SKUing = str(p_sku.location) + str(p_sku.item)
                p_id = sku_id_pairs.setdefault(
                    p_sku, hashlib.sha256(parent_SKUing.encode()).hexdigest()
                )
                parent_ids.add(p_id)

            id_prefix = "id_"  # so ID always starts with letters
            record = {
                "id": id_prefix + sku_id,
                "location": sku.location,
                "item": sku.item,
                "parents": list(sorted([id_prefix + i for i in parent_ids])),
                "level": ((-1) * (val["sku_level"] - self._highest_level)) + 1,
                "normalised_level": val["sku_level"],
            }

            if attributes:
                for attr in attributes:
                    try:
                        record[attr] = getattr(sku, attr)
                    except Exception as e:
                        print(e)
                        raise


            # Add items without parents at the beginning of the list
            if len(val["parent_skus"]) == 0:
                f_result.appendleft(record)
            else:
                f_result.append(record)

        return list(f_result)



class _SKUType(Enum):
    PARENT = "ultimate parent"
    INTERMEDIATE = "intermediate"
    CHILD = "ultimate child"
    UNDEFINED = "undefined"


class _SKULink:
    __slot__ = ["sku", "qty"]

    def __init__(self, sku: SKU, qty: float):
        if not isinstance(sku, SKU):
            raise TypeError(f"sku must be an SKU instance.")

        self.sku = sku
        self.qty = qty

    def __repr__(self):
        return f"{self.sku}"

    @property
    def qty(self):
        return self._qty

    @qty.setter
    def qty(self, value):
        if value is None:
            self._qty = 1
            return
        value = convert_to_float(value)

        self._qty = value


class SKU:
    """
    Class for keeping track of an item in inventory.

    Stock keeping unit (SKU) is a unique combination of an item/part code in a
    location.

    It's covers products to costumers, assemblies and purchased
    materials.

    Note
    ----
    Current location is always in the output of properties and functions.
    Because sometimes different factories have the same item/part code.

    """

    __slot__ = ["item", "location", "sellable", "phantom", "obsolete", "_type", "status", "_abc_classifications", "abc_classification", "safety_stock_qty", "lead_time", "inventory_qty", "minimum_order_qty", "batch_size", "_child_links", "_parent_links", "_pptree_parents", "_pptree_children"]

    classification_rank = {
        "AX": 90,
        "AY": 80,
        "AZ": 70,
        "BX": 60,
        "BY": 50,
        "BZ": 40,
        "CX": 30,
        "CY": 20,
        "CZ": 10,
        "NA": 00,
    }

    def __init__(
        self,
        item,
        location: str = None,
        inventory_qty: float = 0,
        minimum_order_qty: float = 0,
        batch_size: float = 0,
        maximum_order_qty: float = 0,
        safety_stock_qty: float = 0,
        lead_time: int = 0,
        abc_classification="NA",
        status: str = None,
        sellable: bool = False,
        phantom: bool = False,
        obsolete: bool = False,
    ):
        # Keys
        if not isinstance(item, str):
            raise TypeError(f"Bad type for '{item}': item must be a string, not a {type(item)}")
        if not item:
            raise ValueError(f"Item '{item}' must be a non-empty string.")
        self.item = item.strip().upper()

        if location is not None:
            if not isinstance(location, str):
                raise TypeError(f"Bad type for: '{location}': location must be a string, not a {type(location)}")
            if not location:
                raise ValueError(f"Location '{location}' must be a non-empty string.")
            location = location.strip().upper()
        self.location = location

        # Qualitative fields
        self.sellable = sellable
        self.phantom = phantom
        self.obsolete = obsolete
        self.status = status 
        self.abc_classification = abc_classification
        self._type = _SKUType.UNDEFINED

        # Numerical fields
        self.safety_stock_qty = safety_stock_qty
        self.lead_time = lead_time
        self.inventory_qty = inventory_qty
        self.minimum_order_qty = minimum_order_qty
        self.batch_size = batch_size
        self.maximum_order_qty = maximum_order_qty

        # Links between the items
        self._child_links: List[_SKULink] = []
        self._parent_links: List[_SKULink] = []

        # Links between the items (only for pptree library)
        self._pptree_parents: List[SKU] = []
        self._pptree_children: List[SKU] = []

    def __repr__(self):
        return f"SKU(location={self.location}, item={self.item})"

    def __str__(self):
        output = f"{self.item}"
        if self.location:
            output + f" at {self.location}"

        return output

    def __eq__(self, other):
        if isinstance(other, SKU):
            return (self.location, self.item) == (other.location, other.item)
        return False

    def __hash__(self):
        return hash((self.location, self.item))


    @property
    def children(self):
        """Returns all the immediate child items."""
        output = set()
        for child_link in self._child_links:
            output.add(child_link.sku)

        return output
    
    @property
    def active_children(self):
        """Returns all the child items that are not obsoleted."""
        output = set()
        for child_link in self._child_links:
            if not child_link.sku.obsolete:
                output.add(child_link.sku)

        return output

    @property
    def child_links(self):
        """Returns all the immediate child items along with the quantities."""
        return self._child_links
    
    @property
    def child_skus(self):
        return {links.sku for links in self._child_links}

    @property
    def ultimate_children(self):
        """Return all the lowermost/lowest child items in this bill of materials.
        
        Note: list may contain duplicate parent items.
        """
        return self._get_leaf_nodes("children")

    @property
    def all_children(self):
        """Return all the child items in the bill of materials (from immediate to ultimate items)"""
        return self._level_order_traverse("children")

    @property
    def parents(self):
        """Returns all the immediate parent items."""
        output = set()
        for parent_link in self._parent_links:
            output.add(parent_link.sku)

        return output

    @property
    def active_parents(self):
        """Returns all the child items that are not obsoleted."""
        output = set()
        for parent_link in self._parent_links:
            if not parent_link.sku.obsolete:
                output.add(parent_link.sku)

        return output

    @property
    def parent_links(self):
        """Returns all the immediate parent items along with the quantities."""
        return self._parent_links

    @property
    def ultimate_parents(self):
        """Return all the topmost/highest parent items in this bill of materials.
        
        Note: list may contain duplicate parent items.
        """
        return self._get_leaf_nodes("parents")

    @property
    def all_parents(self):
        """Return all the parent items in the bill of materials (from immediate to ultimate items)"""
        return self._level_order_traverse("parents")

    @property
    def inventory_qty(self):
        """Get the value of inventory_qty qty."""
        return self._inventory_qty

    @inventory_qty.setter
    def inventory_qty(self, value):
        try:
            value = float(value)
        except TypeError:
            print("minimum order qty must be an integer or a float.")
            raise
        self._inventory_qty = float(value)

    @property
    def minimum_order_qty(self):
        """Get the value of minimum order qty."""
        return self._minimum_order_qty

    @minimum_order_qty.setter
    def minimum_order_qty(self, value):
        """Set the value of minimum order qty."""
        try:
            value = float(value)
        except TypeError:
            print("minimum order qty must be an integer or a float.")
            raise

        if value < 0:
            raise ValueError(f"minimum order qty must be a positive number.")

        self._minimum_order_qty = value


    @property
    def maximum_order_qty(self):
        """Get the value of maximum order qty."""
        return self._maximum_order_qty

    @maximum_order_qty.setter
    def maximum_order_qty(self, value):
        """Set the value of maximum order qty."""
        try:
            value = float(value)
        except TypeError:
            print("maximum order qty must be an integer or a float.")
            raise

        if value < 0:
            raise ValueError(f"maximum order qty must be a positive number.")

        self._maximum_order_qty = value


    @property
    def batch_size(self):
        """Get the value of rounding value qty."""
        return self._batch_size

    @batch_size.setter
    def batch_size(self, value):
        """Set the value of rounding value qty."""
        try:
            value = float(value)
        except TypeError:
            print("rounding value qty must be an integer or a float.")
            raise

        if value < 0:
            raise ValueError(f"rounding value qty must be a positive number.")

        self._batch_size = float(value)

    @property
    def safety_stock_qty(self):
        """Get the value of safety stock qty."""
        return self._safety_stock_qty

    @safety_stock_qty.setter
    def safety_stock_qty(self, value):
        """Set the value of safety stock qty."""
        try:
            value = float(value)
        except TypeError:
            print("safety stock qty must be an integer or a float.")
            raise

        if value < 0:
            raise ValueError(f"safety stock qty must be a positive number.")

        self._safety_stock_qty = float(value)

    @property
    def lead_time(self):
        """Get the value of lead time."""
        return self._lead_time

    @lead_time.setter
    def lead_time(self, value):
        """Set the value of lead time."""
        try:
            value = float(value)
        except TypeError:
            print("lead time must be an integer or a float.")
            raise

        if value < 0:
            raise ValueError(f"lead time must be a positive number.")

        self._lead_time = int(value)

    @property
    def type(self):
        return self._type.value

    @type.setter
    def type(self, value: _SKUType):
        """
        It sets the type of the item.

        Parameters
        ----------
        value : _SKUType
            The SKU type PARENT or CHILD. The asssignment logic is then 
            following:

            current   new     result
            -------   ------  -------
            None      parent  parent
            None      child   child
            child     parent  intermediate
            child     child   child
            parent    parent  parent
            parent    child   intermediate
            
        Raises
        ------
        TypeError
            If the value is not an instance of the _SKUType class.
        ValueError
            If the SKU type is different than PARENT or CHILD.

        """

        if not isinstance(value, _SKUType):
            raise TypeError(
                f"Argument must be of type NodeType.\nYour value is:{value} and type: {type(value)}"
            )

        if value == _SKUType.INTERMEDIATE:
            raise ValueError(
                f"You can only assign the values: PARENT and CHILD.\nYour value is: {value.name}"
            )

        if value != self._type:
            if self._type == _SKUType.UNDEFINED:
                self._type = value
            else:
                self._type = _SKUType.INTERMEDIATE


    def _level_order_traverse(self, direction):
        # try to get the attribute
        if getattr(self, direction) is None:
            raise AttributeError(
                f"Attribute {direction} not found in class {self.__class__.__name__}"
            )

        stack = list(getattr(self, direction))  # self should not be in the output
        result = []

        while stack:
            node = stack.pop()
            result.append(node)

            for nodes in getattr(node, direction):
                stack.append(nodes)

        return result

    def _get_leaf_nodes(self, direction):
        if getattr(self, direction) is None:
            raise AttributeError(
                f"Attribute {direction} not found in class {self.__class__.__name__}"
            )

        stack = getattr(self, direction)
        root_nodes = []

        while stack:
            node = stack.pop()
            if len(getattr(node, direction)) == 0:
                root_nodes.append(node)
            else:
                for sku in getattr(node, direction):
                    stack.add(sku)

        return root_nodes


    @property
    def abc_classification(self):
        return self._abc_classification

    @abc_classification.setter
    def abc_classification(self, value: str):
        """
        Sets the value for abc_classification

        Parameters
        ----------
        value : str
            value (str): the length must be two and the first letter must be
            either A, B, or C and the second letter must be X, Y, or Z. And it
            will only be assigned if the classification is higher
            
            e.g.:
                AX
                AY
                BZ
                CZ

        Raises
        ------
        ValueError
            If value is not a valid one.

        """
        new_classification = self.classification_rank.get(value)
        if new_classification is None:
            raise ValueError(
                f"Value '{new_classification}' not found in classifications."
            )
        
        if not hasattr(self, "_abc_classification"):
            self._abc_classification = "NA"
  
        if self._is_classification_higher(self.abc_classification, value):
            self._abc_classification = value
            self._propagate_classifications_down(value)

    @property
    def sellable(self):
        return self._sellable

    @sellable.setter
    def sellable(self, value):
        if not isinstance(value, bool):
            raise TypeError(f"Bad Type: input must be a boolean, not a '{type(value)}'.")
        self._sellable = value

    def _propagate_classifications_down(self, new_value: str):
        """
        Propagate the new clasification for the item down to their children and
        update the childrens classification, if needed.

        Classification is updated only when the new classification has a higher
        score than the current one.

        Parameters
        ----------
        value : str
            The new classification for the item.

        """
        queue = [self]

        while queue:
            for _ in range(len(queue)):
                node = queue.pop()

                if self._is_classification_higher(node.abc_classification, new_value):
                    node.abc_classification = new_value

                for child_link in node._child_links:
                    queue.append(child_link.sku)

    def _is_classification_higher(self, current, new):
        return self.classification_rank[current] < self.classification_rank[new]

    def get_missing_safety_stock_qty(self):
        if self.inventory_qty < 0:
            return self.safety_stock_qty

        if self.inventory_qty < self.safety_stock_qty:
            return self.safety_stock_qty - self.inventory_qty
        else:
            return 0

    def _adjust_qty_to_moq_and_batch(self, order_qty: int | float) -> repleno._Order:
        """
        Rounds the quantity according to the minimum order qty and batch size of the SKU.

        Parameters
        ----------
        order_qty : int | float
            Quantity to be lot sized.

        Returns
        -------
        _Order
            Order with the adjusted quantity

        """

        if order_qty == 0:
            return 0

        if order_qty <= self.minimum_order_qty:
            return self.minimum_order_qty

        if not self.batch_size:
            return order_qty

        order_qty_diff = order_qty - self.minimum_order_qty  
        above_moq_qty = math.ceil(order_qty_diff / self.batch_size) * self.batch_size

        return self.minimum_order_qty + above_moq_qty


    def _link_child(self, child_sku, qty=1):
        """
        Internal Method to be used exclusively by the Factory class. This is
        because the Factory needs to register it to keep track of all the
        items.
        """

        if not isinstance(child_sku, SKU):
            raise TypeError(f"Bad type: child_sku argument must be {type(SKU)}")

        if self.item == child_sku.item and self.location == child_sku.location:
            warnings.warn(f"SKU cannot be linked to itself.")
            return 

        try:
            qty = convert_to_float(qty)
        except Exception as e:
            print(f"'{qty}' was not able to be converted to a float number.")
            raise
 
        self._check_for_recursion(child_sku)
        self._update_types(child_sku)
        self._update_sellable_flag(child_sku)
        self._add_child_for_pptree_visualisation(child_sku)

        # Link both ways: parent > child and child > parent
        if not isinstance(qty, (float, int)):
            raise TypeError(f"qty must be a float number.")

        self._child_links.append(_SKULink(child_sku, qty))
        child_sku._parent_links.append(_SKULink(self, 0 if qty == 0 else 1 / qty))


    def _check_for_recursion(self, child_node):
        if child_node in self.all_parents:
            raise ValueError(
                f"Linking the child '{child_node.item}' to the parent '{self.item}' resulted in recursion."
            )

    def _update_types(self, child_node):
        # NOTE: the property type must be used for validation, not "_type"
        self.type = _SKUType.PARENT  
        child_node.type = _SKUType.CHILD 

    def _update_sellable_flag(self, child_node):
        if self._type == _SKUType.PARENT:
            self.sellable = True

        if child_node._type == _SKUType.PARENT:
            self.sellable = True

    def _add_child_for_pptree_visualisation(self, child_node):
        child_node._pptree_parents.append(self)
        self._pptree_children.append(child_node)

    def show(self, direction="children"):
        if direction not in ["children", "parents"]:
            raise ValueError('direction arg must be "children" or "parents"')
        else:
            # second argument is property name of Node that holds next node
            pptree.print_tree(self, childattr="_pptree_" + direction)


    def _are_levels_equal(self, node, direction, past_node=None):
        anti_direction = "parents" if direction == "children" else "children"

        if not self and not node:
            # both nodes are empty, so they're equal
            return True
        elif not self or not node:
            # one node is empty and the other is not, so they're not equal
            return False
        elif self.item != node.item:
            # the nodes have different values, so the trees are not equal
            return False
        elif len(getattr(self, direction)) != len(getattr(node, direction)):
            # the nodes have different numbers of children, so the trees are not equal
            return False
        elif past_node is not None and len(getattr(self, anti_direction)) > 1:
            # recursively check the children of the parents or the parents of the children
            # perform the check in the other direction
            # get nodes in the other direction but remove the previous one
            # (where it's coming from) to avoid infine recursion
            # (bouncing back and forth between child-parent)
            next_nodes = getattr(self, anti_direction)
            next_nodes.remove(past_node)

            other_next_nodes = getattr(node, anti_direction)
            return self._move_to_next_level(
                next_nodes, other_next_nodes, anti_direction
            )

        else:
            # recursively check if each parent/child of node1 is equal to any
            # parent/child of node2
            next_nodes = getattr(self, direction)
            other_next_nodes = getattr(node, direction)
            return self._move_to_next_level(next_nodes, other_next_nodes, direction)

    def _move_to_next_level(self, next_nodes, other_next_nodes, direction):
        for next_node in next_nodes:
            found_match = False
            for other_next_node in other_next_nodes:
                if next_node._are_levels_equal(other_next_node, direction, self):
                    found_match = True
                    break
            if not found_match:
                return False
        return True

    def is_tree_equal(self, node):
        """
        Recursively checks all children and parents to see if self and node
        parameter belong to a tree with the same item codes.

        Args:
            node (Item): Second that self is compared to.

        Returns:
            bool: True if all tree is equal, False otherwise.

        """
        upwards = self._are_levels_equal(node, "parents")
        downwards = self._are_levels_equal(node, "children")

        return upwards and downwards



    def get_lineage(
        self,
        include_obsoletes=True,
        attributes=None,
        max_stack_size=None,
    ):
        """
        It gets all the parents and children of a location + item code.

        It returns a list of dictionaries containing the following keys:
        {
            "id": the hashed string of location + item,
            "location": the location code,
            "item": the item code,
            "parents": the ID's of the immediate parents,
            "children": the ID's of the immediate children,
            "stocking_type": the stocking type,
            "level": starts at 0 with root items and increases by +1,
        }

        The parents list contains only items that have id's
        """

        # Breadth-first traversal (BFS) is used because it's easier to think
        # about the logic by levels
        
        output = _OutputFormatter(max_stack_size=max_stack_size)

        # add current items and iterate over the children
        # ===============================================
        if not include_obsoletes and self.obsolete:
            return []

        selected_parents = self.parents if include_obsoletes else self.active_parents
        queue = [(selected_parents, self, 0)]  # (previous_sku, current_sku, level)
        while queue:
            for _ in range(len(queue)):
                sku_ancestor, sku, level = queue.pop(0)

                selected_children = sku.child_skus if include_obsoletes else sku.active_children

                output.store(
                    sku=sku,
                    parent_skus=sku_ancestor,
                    child_skus=selected_children,
                    level=level,
                    direction="children",
                )

                for c_sku in selected_children:
                    queue.append((sku, c_sku, level - 1))

        # iterate over the parents
        # ==========================
        # get parent nodes from node

        selected_children = self.child_skus if include_obsoletes else self.active_children
        queue = [(selected_children, self, 0)]
        while queue:
            for _ in range(len(queue)):
                sku_ancestor, sku, level = queue.pop(0)

                selected_parents = sku.parents if include_obsoletes else sku.active_parents

                output.store(
                    sku=sku,
                    parent_skus=selected_parents,
                    child_skus=sku_ancestor,
                    level=level,
                    direction="parents",
                )

                for p_sku in selected_parents:
                    queue.append((sku, p_sku, level + 1))

        return output.get_output(attributes=attributes)


    def get_collaterals(
        self,
        include_obsoletes=False,
        items_only=False,
        attributes=None,
        max_stack_size=None,
        phaseout_skus=None,
        child_only=False,
    ):
        """
        It generates a list of all items identified as collaterals. 
        An item is considered collateral if it meets the following criteria:
            1. Items that use item_code as input material for their production;
            2. Items that are used as input material for item_code's production;
            3. Any indirect items that satisfy points 1 or 2.

        Parameters
        ----------
        include_obsoletes : bool, optional
            Obsolete items are not considered when gathering the collaterals, by
            default False
            
        items_only : bool, optional
            Returns a list of items that are identified as collaterals, instead
            of a list of SKUs. By default False.
            
        attributes : list[str], optional
            Returns the list of dictionaries including the SKU attributes
            specified here. The attributes here must match the SKU attribute
            names, by default None
            
        max_stack_size : int, optional
            If the amount of collaterals collected exceeds the `max_stack_size`,
            a BufferError is thrown. This is useful when the BOM is too large
            and the method takes too long to run. By default None

        only_child : bool, optional
            If set to `True`, it ignores all parent items and scan only for
            child collaterals. By default False

        phaseout_skus : list, optional



        Returns
        -------
        list
            If no parameter is passed that changes the output, it returns a list
            of dictionaries with the following keys:
                - ID;
                - location: location of target item;
                - item: target item;
                - parents: immediate parents;
                - level: The target item is assigned a value of 0, while its
                children are assigned negative numbers (-1, -2, -3..) based on
                their depth in the BOM, and its parents are assigned positive
                numbers (+1, +2, +3...) based on their height;
                
            Note that the list is self-contained in the sense that all parents
            have their own IDs in the output.
            
            If items_only = True, it returns a list with the collateral items.

            If child_only = True, it searches for collaterals looking only at
            the child items.
        
        """

        # Breadth-first traversal (BFS) is used because it's easier to think
        # about the logic by levels

        if not phaseout_skus:
            phaseout_skus = set()

        if not include_obsoletes and self.obsolete:
            return []

        output = _OutputFormatter(max_stack_size=max_stack_size) 

        if not child_only:
            output = self._scan_parents(
                collaterals=output,
                include_obsoletes=include_obsoletes,
                phaseout_set=phaseout_skus
            )

        output = self._scan_children(
            collaterals=output,
            level=0,
            include_obsoletes=include_obsoletes,
            phaseout_set=phaseout_skus
        )

        return output.get_output(items_only, attributes)

    def _scan_parents(self, collaterals, include_obsoletes, phaseout_set):
        p_collaterals = collaterals

        # Get following nodes
        selected_parents = self.parents if include_obsoletes else self.active_parents
        # Remove any SKU that is already in collaterals
        selected_parents = selected_parents - collaterals._skus        
        # enqueue (previous_sku, current_sku, level)
        queue = [(self, sku, 1) for sku in selected_parents]  
        while queue:
            for _ in range(len(queue)):
                sku_ancestor, sku, level = queue.pop(0)

                # Filter out obsoletes if needed
                selected_parents = sku.parents if include_obsoletes else sku.active_parents

                # Add sku to collaterals
                p_collaterals.store(
                    sku=sku,
                    parent_skus=selected_parents,
                    child_skus=sku_ancestor,
                    level=level,
                    direction="parents",
                )

                # Scan the children and add the result to p_collaterals
                p_collaterals = sku._scan_children(
                    collaterals=p_collaterals, 
                    level=level, 
                    include_obsoletes=include_obsoletes,
                    phaseout_set=phaseout_set
                )

                for parent_node in selected_parents:
                    queue.append((sku, parent_node, level + 1))

        return p_collaterals

    def _scan_children(self, collaterals, level, include_obsoletes, phaseout_set):
        """
        Check if child items should be part of collaterals when self is being
        obsoleted
        """

        # Get following nodes
        selected_children = self.children if include_obsoletes else self.active_children
        # Remove any SKU that is already in collaterals
        selected_children = selected_children - collaterals._skus        
        # enqueue (previous_sku, current_sku, level)
        queue = [(self, sku, level - 1) for sku in selected_children]    
        while queue:
            for _ in range(len(queue)):
                sku_ancestor, sku, level = queue.pop(0)

                # Logic to see if child should be added
                unique_parent = len(sku.parents) <= 1
                endoflife_items = set(collaterals._skus).union(phaseout_set)
                all_parents_in_endoflife = not bool(set(sku.parents) - endoflife_items)

                add_children = (unique_parent or all_parents_in_endoflife) and not sku.sellable

                if add_children:
                    # Filter out obsoletes if needed
                    selected_children = sku.children if include_obsoletes else sku.active_children
                    selected_children = selected_children - collaterals._skus

                    # Add child to collaterals
                    collaterals.store(
                        sku=sku,
                        parent_skus=sku_ancestor,
                        child_skus=selected_children,
                        level=level,
                        direction="children",
                    )

                    # Move to next children
                    for child_node in selected_children:
                        if not collaterals.records.get(child_node):
                            queue.append((sku, child_node, level - 1))
        
        return collaterals