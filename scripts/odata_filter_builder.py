'''
OData Filter Builder for Windchill REST API

Builds OData $filter expressions compliant with PTC Windchill REST Services.
Based on: https://support.ptc.com/help/windchill_rest_services/r2.7/en/index.html

Supported OData Expressions:
- Data types: String, Int16, Int32, Int64, Boolean, DateTimeOffset, Single, Double
- Comparison operators: eq, ne, gt, lt, ge, le
- Logical operators: and, or, not
- String methods: startswith, endswith, contains
- Type checking: isof
- Special properties: ID, CreatedBy, ModifiedBy, View

Usage:
    from odata_filter_builder import ODataFilter
    
    # Simple filters
    f = ODataFilter()
    f.eq("Number", "V0056726").and_eq("State", "RELEASED")
    filter_str = f.build()  # "Number eq 'V0056726' and State eq 'RELEASED'"
    
    # Complex filters
    f = (ODataFilter().eq("State", "RELEASED")
                      .and_contains("Name", "Bracket")
                      .or_(ODataFilter().gt("Quantity", 100)
                                        .and_lt("Quantity", 500)))
    
    # Using convenience methods
    from odata_filter_builder import Filter
    expr = Filter.and_(
        Filter.eq("State", "RELEASED"),
        Filter.or_(
            Filter.contains("Name", "Bracket"),
            Filter.startswith("Number", "ASM")
        )
    )
'''
# Copyright 2025 Windchill PLM Client Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re
from datetime import datetime, date
from typing import Any, List, Optional, Union
from enum import Enum


class ODataType(Enum):
    """OData data types supported by Windchill REST API."""
    STRING = "Edm.String"
    INT16 = "Edm.Int16"
    INT32 = "Edm.Int32"
    INT64 = "Edm.Int64"
    BOOLEAN = "Edm.Boolean"
    DATETIME = "Edm.DateTimeOffset"
    SINGLE = "Edm.Single"
    DOUBLE = "Edm.Double"
    DECIMAL = "Edm.Decimal"
    GUID = "Edm.Guid"


class ODataFilter:
    """
    Builder for OData $filter expressions.
    
    Provides a fluent interface for constructing complex filter expressions
    that comply with PTC Windchill REST Services OData implementation.
    
    Example:
        >>> f = ODataFilter()
        >>> f.eq("Number", "V0056726")
        >>> f.and_contains("Name", "Bracket")
        >>> f.build()
        "Number eq 'V0056726' and contains(Name, 'Bracket')"
    """
    
    def __init__(self, expression: str = ""):
        """Initialize filter builder with optional starting expression."""
        self._expression = expression
        self._parts: List[str] = []
        if expression:
            self._parts.append(expression)
    
    # =========================================================================
    # Value Formatting
    # =========================================================================
    
    @staticmethod
    def format_string(value: str) -> str:
        """Format a string value for OData (escapes single quotes)."""
        escaped = str(value).replace("'", "''")
        return f"'{escaped}'"
    
    @staticmethod
    def format_boolean(value: bool) -> str:
        """Format a boolean value for OData."""
        return "true" if value else "false"
    
    @staticmethod
    def format_datetime(value: Union[datetime, date, str]) -> str:
        """
        Format a datetime value for OData.
        
        Args:
            value: datetime object, date object, or ISO format string
            
        Returns:
            OData datetime format: datetime'YYYY-MM-DDThh:mm:ssZ'
        """
        if isinstance(value, datetime):
            # Use UTC format
            iso_str = value.strftime("%Y-%m-%dT%H:%M:%SZ")
        elif isinstance(value, date):
            iso_str = value.strftime("%Y-%m-%dT00:00:00Z")
        else:
            # Assume ISO string, ensure Z suffix
            iso_str = str(value)
            if not iso_str.endswith('Z'):
                iso_str = iso_str.rstrip() + 'Z'
        return f"datetime'{iso_str}'"
    
    @staticmethod
    def format_guid(value: str) -> str:
        """Format a GUID value for OData."""
        return f"guid'{value}'"
    
    @staticmethod
    def format_number(value: Union[int, float]) -> str:
        """Format a numeric value for OData."""
        return str(value)
    
    @staticmethod
    def format_value(value: Any, data_type: ODataType = None) -> str:
        """
        Auto-detect and format a value for OData.
        
        Args:
            value: The value to format
            data_type: Optional explicit type override
            
        Returns:
            Properly formatted OData value string
        """
        if value is None:
            return "null"
        
        # Explicit type override
        if data_type:
            if data_type in (ODataType.STRING,):
                return ODataFilter.format_string(value)
            elif data_type in (ODataType.INT16, ODataType.INT32, ODataType.INT64):
                return ODataFilter.format_number(int(value))
            elif data_type in (ODataType.SINGLE, ODataType.DOUBLE, ODataType.DECIMAL):
                return ODataFilter.format_number(float(value))
            elif data_type == ODataType.BOOLEAN:
                return ODataFilter.format_boolean(bool(value))
            elif data_type == ODataType.DATETIME:
                return ODataFilter.format_datetime(value)
            elif data_type == ODataType.GUID:
                return ODataFilter.format_guid(str(value))
        
        # Auto-detect type
        if isinstance(value, bool):
            return ODataFilter.format_boolean(value)
        elif isinstance(value, (int, float)):
            return ODataFilter.format_number(value)
        elif isinstance(value, datetime):
            return ODataFilter.format_datetime(value)
        elif isinstance(value, date):
            return ODataFilter.format_datetime(value)
        else:
            return ODataFilter.format_string(str(value))
    
    # =========================================================================
    # Comparison Operators (eq, ne, gt, lt, ge, le)
    # =========================================================================
    
    def eq(self, property_name: str, value: Any, data_type: ODataType = None) -> 'ODataFilter':
        """Add equality comparison: property eq value."""
        formatted = self.format_value(value, data_type)
        self._parts.append(f"{property_name} eq {formatted}")
        return self
    
    def ne(self, property_name: str, value: Any, data_type: ODataType = None) -> 'ODataFilter':
        """Add inequality comparison: property ne value."""
        formatted = self.format_value(value, data_type)
        self._parts.append(f"{property_name} ne {formatted}")
        return self
    
    def gt(self, property_name: str, value: Any, data_type: ODataType = None) -> 'ODataFilter':
        """Add greater-than comparison: property gt value."""
        formatted = self.format_value(value, data_type)
        self._parts.append(f"{property_name} gt {formatted}")
        return self
    
    def lt(self, property_name: str, value: Any, data_type: ODataType = None) -> 'ODataFilter':
        """Add less-than comparison: property lt value."""
        formatted = self.format_value(value, data_type)
        self._parts.append(f"{property_name} lt {formatted}")
        return self
    
    def ge(self, property_name: str, value: Any, data_type: ODataType = None) -> 'ODataFilter':
        """Add greater-than-or-equal comparison: property ge value."""
        formatted = self.format_value(value, data_type)
        self._parts.append(f"{property_name} ge {formatted}")
        return self
    
    def le(self, property_name: str, value: Any, data_type: ODataType = None) -> 'ODataFilter':
        """Add less-than-or-equal comparison: property le value."""
        formatted = self.format_value(value, data_type)
        self._parts.append(f"{property_name} le {formatted}")
        return self
    
    # =========================================================================
    # Logical Operators (and, or, not)
    # =========================================================================
    
    def and_(self, other: Union['ODataFilter', str] = None) -> 'ODataFilter':
        """
        Combine with another filter using AND.
        
        If called without arguments, combines existing parts with AND.
        If called with another filter, combines self with that filter.
        """
        if other is None:
            # Combine existing parts
            if len(self._parts) > 1:
                combined = f"({' and '.join(self._parts)})" if len(self._parts) > 1 else self._parts[0]
                self._parts = [combined]
            return self
        else:
            # Combine with another filter
            other_expr = other.build() if isinstance(other, ODataFilter) else other
            self_expr = self.build()
            return ODataFilter(f"({self_expr} and {other_expr})")
    
    def or_(self, other: Union['ODataFilter', str] = None) -> 'ODataFilter':
        """
        Combine with another filter using OR.
        
        If called without arguments, combines existing parts with OR.
        If called with another filter, combines self with that filter.
        """
        if other is None:
            if len(self._parts) > 1:
                combined = f"({' or '.join(self._parts)})" if len(self._parts) > 1 else self._parts[0]
                self._parts = [combined]
            return self
        else:
            other_expr = other.build() if isinstance(other, ODataFilter) else other
            self_expr = self.build()
            return ODataFilter(f"({self_expr} or {other_expr})")
    
    def not_(self) -> 'ODataFilter':
        """Apply NOT operator to the current expression."""
        if self._parts:
            combined = self.build()
            self._parts = [f"not({combined})"]
        return self
    
    # Fluent aliases for chaining
    def and_eq(self, property_name: str, value: Any, data_type: ODataType = None) -> 'ODataFilter':
        """Add AND equality: existing and property eq value."""
        return self._add_logical("and", "eq", property_name, value, data_type)
    
    def or_eq(self, property_name: str, value: Any, data_type: ODataType = None) -> 'ODataFilter':
        """Add OR equality: existing or property eq value."""
        return self._add_logical("or", "eq", property_name, value, data_type)
    
    def and_ne(self, property_name: str, value: Any, data_type: ODataType = None) -> 'ODataFilter':
        """Add AND inequality: existing and property ne value."""
        return self._add_logical("and", "ne", property_name, value, data_type)
    
    def or_ne(self, property_name: str, value: Any, data_type: ODataType = None) -> 'ODataFilter':
        """Add OR inequality: existing or property ne value."""
        return self._add_logical("or", "ne", property_name, value, data_type)
    
    def and_gt(self, property_name: str, value: Any, data_type: ODataType = None) -> 'ODataFilter':
        """Add AND greater-than: existing and property gt value."""
        return self._add_logical("and", "gt", property_name, value, data_type)
    
    def or_gt(self, property_name: str, value: Any, data_type: ODataType = None) -> 'ODataFilter':
        """Add OR greater-than: existing or property gt value."""
        return self._add_logical("or", "gt", property_name, value, data_type)
    
    def and_lt(self, property_name: str, value: Any, data_type: ODataType = None) -> 'ODataFilter':
        """Add AND less-than: existing and property lt value."""
        return self._add_logical("and", "lt", property_name, value, data_type)
    
    def or_lt(self, property_name: str, value: Any, data_type: ODataType = None) -> 'ODataFilter':
        """Add OR less-than: existing or property lt value."""
        return self._add_logical("or", "lt", property_name, value, data_type)
    
    def and_ge(self, property_name: str, value: Any, data_type: ODataType = None) -> 'ODataFilter':
        """Add AND greater-or-equal: existing and property ge value."""
        return self._add_logical("and", "ge", property_name, value, data_type)
    
    def or_ge(self, property_name: str, value: Any, data_type: ODataType = None) -> 'ODataFilter':
        """Add OR greater-or-equal: existing or property ge value."""
        return self._add_logical("or", "ge", property_name, value, data_type)
    
    def and_le(self, property_name: str, value: Any, data_type: ODataType = None) -> 'ODataFilter':
        """Add AND less-or-equal: existing and property le value."""
        return self._add_logical("and", "le", property_name, value, data_type)
    
    def or_le(self, property_name: str, value: Any, data_type: ODataType = None) -> 'ODataFilter':
        """Add OR less-or-equal: existing or property le value."""
        return self._add_logical("or", "le", property_name, value, data_type)
    
    def _add_logical(self, logical: str, operator: str, 
                     property_name: str, value: Any, data_type: ODataType = None) -> 'ODataFilter':
        """Helper to add a logical operator with comparison."""
        formatted = self.format_value(value, data_type)
        expr = f"{property_name} {operator} {formatted}"
        if self._parts:
            combined = f"{' and '.join(self._parts)} {logical} {expr}"
            self._parts = [combined]
        else:
            self._parts.append(expr)
        return self
    
    # =========================================================================
    # String Functions (startswith, endswith, contains)
    # =========================================================================
    
    def startswith(self, property_name: str, value: str) -> 'ODataFilter':
        """Add startswith function: startswith(property, 'value')."""
        formatted = self.format_string(value)
        self._parts.append(f"startswith({property_name}, {formatted})")
        return self
    
    def endswith(self, property_name: str, value: str) -> 'ODataFilter':
        """Add endswith function: endswith(property, 'value')."""
        formatted = self.format_string(value)
        self._parts.append(f"endswith({property_name}, {formatted})")
        return self
    
    def contains(self, property_name: str, value: str) -> 'ODataFilter':
        """Add contains function: contains(property, 'value')."""
        formatted = self.format_string(value)
        self._parts.append(f"contains({property_name}, {formatted})")
        return self
    
    def and_startswith(self, property_name: str, value: str) -> 'ODataFilter':
        """Add AND startswith: existing and startswith(property, 'value')."""
        formatted = self.format_string(value)
        expr = f"startswith({property_name}, {formatted})"
        if self._parts:
            combined = f"{' and '.join(self._parts)} and {expr}"
            self._parts = [combined]
        else:
            self._parts.append(expr)
        return self
    
    def or_startswith(self, property_name: str, value: str) -> 'ODataFilter':
        """Add OR startswith: existing or startswith(property, 'value')."""
        formatted = self.format_string(value)
        expr = f"startswith({property_name}, {formatted})"
        if self._parts:
            combined = f"{' or '.join(self._parts)} or {expr}"
            self._parts = [combined]
        else:
            self._parts.append(expr)
        return self
    
    def and_endswith(self, property_name: str, value: str) -> 'ODataFilter':
        """Add AND endswith: existing and endswith(property, 'value')."""
        formatted = self.format_string(value)
        expr = f"endswith({property_name}, {formatted})"
        if self._parts:
            combined = f"{' and '.join(self._parts)} and {expr}"
            self._parts = [combined]
        else:
            self._parts.append(expr)
        return self
    
    def or_endswith(self, property_name: str, value: str) -> 'ODataFilter':
        """Add OR endswith: existing or endswith(property, 'value')."""
        formatted = self.format_string(value)
        expr = f"endswith({property_name}, {formatted})"
        if self._parts:
            combined = f"{' or '.join(self._parts)} or {expr}"
            self._parts = [combined]
        else:
            self._parts.append(expr)
        return self
    
    def and_contains(self, property_name: str, value: str) -> 'ODataFilter':
        """Add AND contains: existing and contains(property, 'value')."""
        formatted = self.format_string(value)
        expr = f"contains({property_name}, {formatted})"
        if self._parts:
            combined = f"{' and '.join(self._parts)} and {expr}"
            self._parts = [combined]
        else:
            self._parts.append(expr)
        return self
    
    def or_contains(self, property_name: str, value: str) -> 'ODataFilter':
        """Add OR contains: existing or contains(property, 'value')."""
        formatted = self.format_string(value)
        expr = f"contains({property_name}, {formatted})"
        if self._parts:
            combined = f"{' or '.join(self._parts)} or {expr}"
            self._parts = [combined]
        else:
            self._parts.append(expr)
        return self
    
    # =========================================================================
    # Type Checking (isof)
    # =========================================================================
    
    def isof(self, type_name: str = None, property_name: str = None) -> 'ODataFilter':
        """
        Add type checking: isof(type) or isof(property, type).
        
        Args:
            type_name: The type to check (e.g., 'WTPart', 'WTDocument')
            property_name: Optional property to check type of
            
        Examples:
            >>> ODataFilter().isof('WTPart')
            "isof('WTPart')"
            
            >>> ODataFilter().isof('WTPart', 'Item')
            "isof(Item, 'WTPart')"
        """
        formatted_type = self.format_string(type_name)
        if property_name:
            self._parts.append(f"isof({property_name}, {formatted_type})")
        else:
            self._parts.append(f"isof({formatted_type})")
        return self
    
    def and_isof(self, type_name: str = None, property_name: str = None) -> 'ODataFilter':
        """Add AND isof type check."""
        formatted_type = self.format_string(type_name)
        if property_name:
            expr = f"isof({property_name}, {formatted_type})"
        else:
            expr = f"isof({formatted_type})"
        if self._parts:
            combined = f"{' and '.join(self._parts)} and {expr}"
            self._parts = [combined]
        else:
            self._parts.append(expr)
        return self
    
    def or_isof(self, type_name: str = None, property_name: str = None) -> 'ODataFilter':
        """Add OR isof type check."""
        formatted_type = self.format_string(type_name)
        if property_name:
            expr = f"isof({property_name}, {formatted_type})"
        else:
            expr = f"isof({formatted_type})"
        if self._parts:
            combined = f"{' or '.join(self._parts)} or {expr}"
            self._parts = [combined]
        else:
            self._parts.append(expr)
        return self
    
    # =========================================================================
    # Special Properties (ID, CreatedBy, ModifiedBy, View)
    # =========================================================================
    
    def by_id(self, object_id: str) -> 'ODataFilter':
        """Filter by ID: ID eq 'object_id'."""
        return self.eq("ID", object_id)
    
    def by_created_by(self, user: str) -> 'ODataFilter':
        """Filter by CreatedBy: CreatedBy eq 'user'."""
        return self.eq("CreatedBy", user)
    
    def by_modified_by(self, user: str) -> 'ODataFilter':
        """Filter by ModifiedBy: ModifiedBy eq 'user'."""
        return self.eq("ModifiedBy", user)
    
    def by_view(self, view_name: str) -> 'ODataFilter':
        """Filter by View: View eq 'view_name'."""
        return self.eq("View", view_name)
    
    # Fluent chaining methods for special properties
    def and_by_id(self, object_id: str) -> 'ODataFilter':
        """Add AND ID filter."""
        return self._add_logical("and", "eq", "ID", object_id)
    
    def or_by_id(self, object_id: str) -> 'ODataFilter':
        """Add OR ID filter."""
        return self._add_logical("or", "eq", "ID", object_id)
    
    def and_by_created_by(self, user: str) -> 'ODataFilter':
        """Add AND CreatedBy filter."""
        return self._add_logical("and", "eq", "CreatedBy", user)
    
    def or_by_created_by(self, user: str) -> 'ODataFilter':
        """Add OR CreatedBy filter."""
        return self._add_logical("or", "eq", "CreatedBy", user)
    
    def and_by_modified_by(self, user: str) -> 'ODataFilter':
        """Add AND ModifiedBy filter."""
        return self._add_logical("and", "eq", "ModifiedBy", user)
    
    def or_by_modified_by(self, user: str) -> 'ODataFilter':
        """Add OR ModifiedBy filter."""
        return self._add_logical("or", "eq", "ModifiedBy", user)
    
    def and_by_view(self, view_name: str) -> 'ODataFilter':
        """Add AND View filter."""
        return self._add_logical("and", "eq", "View", view_name)
    
    def or_by_view(self, view_name: str) -> 'ODataFilter':
        """Add OR View filter."""
        return self._add_logical("or", "eq", "View", view_name)
    
    # =========================================================================
    # Common Filter Patterns
    # =========================================================================
    
    def in_list(self, property_name: str, values: List[Any], data_type: ODataType = None) -> 'ODataFilter':
        """
        Filter where property is in a list of values.
        
        Generates: property eq val1 or property eq val2 or ...
        
        Args:
            property_name: Property to filter on
            values: List of values
            data_type: Optional type for values
        """
        if not values:
            return self
        
        conditions = [f"{property_name} eq {self.format_value(v, data_type)}" for v in values]
        expr = " or ".join(conditions)
        
        if self._parts:
            combined = f"({' and '.join(self._parts)}) and ({expr})"
            self._parts = [combined]
        else:
            self._parts.append(f"({expr})")
        
        return self
    
    def between(self, property_name: str, low: Any, high: Any, 
                data_type: ODataType = None) -> 'ODataFilter':
        """
        Filter where property is between two values (inclusive).
        
        Generates: property ge low and property le high
        """
        formatted_low = self.format_value(low, data_type)
        formatted_high = self.format_value(high, data_type)
        expr = f"{property_name} ge {formatted_low} and {property_name} le {formatted_high}"
        
        if self._parts:
            combined = f"{' and '.join(self._parts)} and ({expr})"
            self._parts = [combined]
        else:
            self._parts.append(f"({expr})")
        
        return self
    
    def is_null(self, property_name: str) -> 'ODataFilter':
        """Filter where property is null: property eq null."""
        self._parts.append(f"{property_name} eq null")
        return self
    
    def is_not_null(self, property_name: str) -> 'ODataFilter':
        """Filter where property is not null: property ne null."""
        self._parts.append(f"{property_name} ne null")
        return self
    
    def and_is_null(self, property_name: str) -> 'ODataFilter':
        """Add AND is-null filter."""
        expr = f"{property_name} eq null"
        if self._parts:
            combined = f"{' and '.join(self._parts)} and {expr}"
            self._parts = [combined]
        else:
            self._parts.append(expr)
        return self
    
    def or_is_null(self, property_name: str) -> 'ODataFilter':
        """Add OR is-null filter."""
        expr = f"{property_name} eq null"
        if self._parts:
            combined = f"{' or '.join(self._parts)} or {expr}"
            self._parts = [combined]
        else:
            self._parts.append(expr)
        return self
    
    def and_is_not_null(self, property_name: str) -> 'ODataFilter':
        """Add AND is-not-null filter."""
        expr = f"{property_name} ne null"
        if self._parts:
            combined = f"{' and '.join(self._parts)} and {expr}"
            self._parts = [combined]
        else:
            self._parts.append(expr)
        return self
    
    def or_is_not_null(self, property_name: str) -> 'ODataFilter':
        """Add OR is-not-null filter."""
        expr = f"{property_name} ne null"
        if self._parts:
            combined = f"{' or '.join(self._parts)} or {expr}"
            self._parts = [combined]
        else:
            self._parts.append(expr)
        return self
    
    # =========================================================================
    # Build Methods
    # =========================================================================
    
    def build(self) -> str:
        """
        Build the final OData filter expression.
        
        Returns:
            OData $filter string ready for URL encoding
        """
        if not self._parts:
            return ""
        
        if len(self._parts) == 1:
            return self._parts[0]
        
        # Default to AND when multiple parts
        return " and ".join(self._parts)
    
    def __str__(self) -> str:
        return self.build()
    
    def __repr__(self) -> str:
        return f"ODataFilter('{self.build()}')"


# =============================================================================
# Convenience Class Methods (Alternative Static API)
# =============================================================================

class Filter:
    """
    Static factory methods for building OData filters.
    
    Provides a functional style alternative to ODataFilter builder.
    
    Example:
        >>> expr = Filter.and_(
        ...     Filter.eq("State", "RELEASED"),
        ...     Filter.or_(
        ...         Filter.contains("Name", "Bracket"),
        ...         Filter.startswith("Number", "ASM")
        ...     )
        ... )
        >>> expr.build()
        "(State eq 'RELEASED') and ((contains(Name, 'Bracket')) or (startswith(Number, 'ASM')))"
    """
    
    @staticmethod
    def eq(property_name: str, value: Any, data_type: ODataType = None) -> ODataFilter:
        """Create equality filter: property eq value."""
        return ODataFilter().eq(property_name, value, data_type)
    
    @staticmethod
    def ne(property_name: str, value: Any, data_type: ODataType = None) -> ODataFilter:
        """Create inequality filter: property ne value."""
        return ODataFilter().ne(property_name, value, data_type)
    
    @staticmethod
    def gt(property_name: str, value: Any, data_type: ODataType = None) -> ODataFilter:
        """Create greater-than filter: property gt value."""
        return ODataFilter().gt(property_name, value, data_type)
    
    @staticmethod
    def lt(property_name: str, value: Any, data_type: ODataType = None) -> ODataFilter:
        """Create less-than filter: property lt value."""
        return ODataFilter().lt(property_name, value, data_type)
    
    @staticmethod
    def ge(property_name: str, value: Any, data_type: ODataType = None) -> ODataFilter:
        """Create greater-or-equal filter: property ge value."""
        return ODataFilter().ge(property_name, value, data_type)
    
    @staticmethod
    def le(property_name: str, value: Any, data_type: ODataType = None) -> ODataFilter:
        """Create less-or-equal filter: property le value."""
        return ODataFilter().le(property_name, value, data_type)
    
    @staticmethod
    def and_(*filters: Union[ODataFilter, str]) -> ODataFilter:
        """Combine filters with AND."""
        if len(filters) == 0:
            return ODataFilter()
        if len(filters) == 1:
            return filters[0] if isinstance(filters[0], ODataFilter) else ODataFilter(filters[0])
        
        parts = [f.build() if isinstance(f, ODataFilter) else f for f in filters]
        return ODataFilter(f"({' and '.join(parts)})")
    
    @staticmethod
    def or_(*filters: Union[ODataFilter, str]) -> ODataFilter:
        """Combine filters with OR."""
        if len(filters) == 0:
            return ODataFilter()
        if len(filters) == 1:
            return filters[0] if isinstance(filters[0], ODataFilter) else ODataFilter(filters[0])
        
        parts = [f.build() if isinstance(f, ODataFilter) else f for f in filters]
        return ODataFilter(f"({' or '.join(parts)})")
    
    @staticmethod
    def not_(filter_: Union[ODataFilter, str]) -> ODataFilter:
        """Apply NOT to a filter."""
        expr = filter_.build() if isinstance(filter_, ODataFilter) else filter_
        return ODataFilter(f"not({expr})")
    
    @staticmethod
    def startswith(property_name: str, value: str) -> ODataFilter:
        """Create startswith filter."""
        return ODataFilter().startswith(property_name, value)
    
    @staticmethod
    def endswith(property_name: str, value: str) -> ODataFilter:
        """Create endswith filter."""
        return ODataFilter().endswith(property_name, value)
    
    @staticmethod
    def contains(property_name: str, value: str) -> ODataFilter:
        """Create contains filter."""
        return ODataFilter().contains(property_name, value)
    
    @staticmethod
    def isof(type_name: str = None, property_name: str = None) -> ODataFilter:
        """Create isof type check."""
        return ODataFilter().isof(type_name, property_name)
    
    @staticmethod
    def in_list(property_name: str, values: List[Any], data_type: ODataType = None) -> ODataFilter:
        """Create in-list filter."""
        return ODataFilter().in_list(property_name, values, data_type)
    
    @staticmethod
    def between(property_name: str, low: Any, high: Any, data_type: ODataType = None) -> ODataFilter:
        """Create between filter (inclusive)."""
        return ODataFilter().between(property_name, low, high, data_type)
    
    @staticmethod
    def is_null(property_name: str) -> ODataFilter:
        """Create is-null filter."""
        return ODataFilter().is_null(property_name)
    
    @staticmethod
    def is_not_null(property_name: str) -> ODataFilter:
        """Create is-not-null filter."""
        return ODataFilter().is_not_null(property_name)


# =============================================================================
# Integration Helper
# =============================================================================

def build_filter(entity_type: str, filters: dict, resolver=None) -> str:
    """
    Build OData filter from dictionary with property name resolution.
    
    This integrates with the property_resolver module for case-insensitive
    property name handling.
    
    Args:
        entity_type: Entity type name (e.g., 'Part', 'Document')
        filters: Dictionary of {property: value} or {property: {'op': operator, 'value': val}}
        resolver: Optional PropertyResolver instance
        
    Returns:
        OData filter string with correct property names
        
    Example:
        >>> build_filter('Part', {'Number': 'V0056726', 'State': 'RELEASED'})
        "Number eq 'V0056726' and State eq 'RELEASED'"
        
        >>> build_filter('Part', {'Quantity': {'ge': 10, 'le': 100}})
        "Quantity ge 10 and Quantity le 100"
    """
    builder = ODataFilter()
    
    # Try to import resolver if not provided
    if resolver is None:
        try:
            from property_resolver import get_resolver
            resolver = get_resolver()
        except ImportError:
            resolver = None
    
    for prop_name, value in filters.items():
        # Resolve property name if resolver available
        if resolver:
            prop_name = resolver.resolve_property(entity_type, prop_name)
        
        # Check for operator specification
        if isinstance(value, dict):
            # Handle {'op': value} format
            for op, val in value.items():
                if op == 'eq':
                    builder.and_eq(prop_name, val)
                elif op == 'ne':
                    builder.and_ne(prop_name, val)
                elif op == 'gt':
                    builder.and_gt(prop_name, val)
                elif op == 'lt':
                    builder.and_lt(prop_name, val)
                elif op == 'ge':
                    builder.and_ge(prop_name, val)
                elif op == 'le':
                    builder.and_le(prop_name, val)
                elif op == 'contains':
                    builder.and_contains(prop_name, val)
                elif op == 'startswith':
                    builder.and_startswith(prop_name, val)
                elif op == 'endswith':
                    builder.and_endswith(prop_name, val)
        else:
            # Simple equality
            builder.and_eq(prop_name, value)
    
    return builder.build()


# =============================================================================
# CLI Test
# =============================================================================

def _test():
    """Test the OData filter builder."""
    print("=" * 70)
    print("OData Filter Builder Tests")
    print("=" * 70)
    
    # Test 1: Simple equality
    print("\n[1] Simple Equality:")
    f = ODataFilter().eq("Number", "V0056726")
    print(f"    Input: eq('Number', 'V0056726')")
    print(f"    Output: {f.build()}")
    
    # Test 2: Multiple conditions with AND
    print("\n[2] Multiple AND Conditions:")
    f = ODataFilter().eq("Number", "V0056726").and_eq("State", "RELEASED")
    print(f"    Input: eq('Number', 'V0056726').and_eq('State', 'RELEASED')")
    print(f"    Output: {f.build()}")
    
    # Test 3: String functions
    print("\n[3] String Functions:")
    f = ODataFilter().startswith("Number", "ASM").or_contains("Name", "Bracket")
    print(f"    Input: startswith('Number', 'ASM').or_contains('Name', 'Bracket')")
    print(f"    Output: {f.build()}")
    
    # Test 4: Comparison operators
    print("\n[4] Comparison Operators:")
    f = ODataFilter().gt("Quantity", 100).and_lt("Quantity", 500)
    print(f"    Input: gt('Quantity', 100).and_lt('Quantity', 500)")
    print(f"    Output: {f.build()}")
    
    # Test 5: NOT operator
    print("\n[5] NOT Operator:")
    f = ODataFilter().eq("State", "RELEASED").not_()
    print(f"    Input: eq('State', 'RELEASED').not_()")
    print(f"    Output: {f.build()}")
    
    # Test 6: isof type checking
    print("\n[6] isof Type Checking:")
    f = ODataFilter().isof("WTPart")
    print(f"    Input: isof('WTPart')")
    print(f"    Output: {f.build()}")
    
    f = ODataFilter().isof("WTPart", "Item")
    print(f"    Input: isof('WTPart', 'Item')")
    print(f"    Output: {f.build()}")
    
    # Test 7: Special properties
    print("\n[7] Special Properties:")
    f = ODataFilter().by_id("OR:wt.part.WTPart:12345")
    print(f"    Input: by_id('OR:wt.part.WTPart:12345')")
    print(f"    Output: {f.build()}")
    
    f = ODataFilter().by_created_by("admin").and_by_modified_by("admin")
    print(f"    Input: by_created_by('admin').and_by_modified_by('admin')")
    print(f"    Output: {f.build()}")
    
    # Test 8: in_list
    print("\n[8] In List:")
    f = ODataFilter().in_list("State", ["RELEASED", "INWORK", "APPROVED"])
    print(f"    Input: in_list('State', ['RELEASED', 'INWORK', 'APPROVED'])")
    print(f"    Output: {f.build()}")
    
    # Test 9: between
    print("\n[9] Between:")
    f = ODataFilter().between("Quantity", 10, 100)
    print(f"    Input: between('Quantity', 10, 100)")
    print(f"    Output: {f.build()}")
    
    # Test 10: DateTime
    print("\n[10] DateTime:")
    from datetime import datetime
    dt = datetime(2024, 1, 15, 10, 30, 0)
    f = ODataFilter().gt("CreatedOn", dt)
    print(f"    Input: gt('CreatedOn', datetime(2024, 1, 15, 10, 30, 0))")
    print(f"    Output: {f.build()}")
    
    # Test 11: Boolean
    print("\n[11] Boolean:")
    f = ODataFilter().eq("IsPrimary", True)
    print(f"    Input: eq('IsPrimary', True)")
    print(f"    Output: {f.build()}")
    
    # Test 12: Complex nested expression
    print("\n[12] Complex Nested Expression:")
    f = (ODataFilter()
         .eq("State", "RELEASED")
         .and_(ODataFilter()
               .contains("Name", "Bracket")
               .or_startswith("Number", "ASM")))
    print(f"    Input: eq('State', 'RELEASED').and_(contains('Name', 'Bracket').or_startswith('Number', 'ASM'))")
    print(f"    Output: {f.build()}")
    
    # Test 13: Static Filter API
    print("\n[13] Static Filter API:")
    f = Filter.and_(
        Filter.eq("State", "RELEASED"),
        Filter.or_(
            Filter.contains("Name", "Bracket"),
            Filter.startswith("Number", "ASM")
        )
    )
    print(f"    Input: Filter.and_(eq('State', 'RELEASED'), or_(contains('Name', 'Bracket'), startswith('Number', 'ASM')))")
    print(f"    Output: {f.build()}")
    
    # Test 14: Null handling
    print("\n[14] Null Handling:")
    f = ODataFilter().is_null("Description").or_is_not_null("ReviewDate")
    print(f"    Input: is_null('Description').or_is_not_null('ReviewDate')")
    print(f"    Output: {f.build()}")
    
    print("\n" + "=" * 70)
    print("All tests completed!")
    print("=" * 70)


if __name__ == '__main__':
    _test()
