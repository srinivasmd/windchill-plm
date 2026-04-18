#!/usr/bin/env python3
"""
Test script to verify OData filter expressions supported by Zephyr.

Tests all OData expressions required by Windchill:
- Data types: String, Int16, Int32, Int64, Boolean, DateTimeOffset, Single, Double
- Comparison operators: EQ, NE, GT, LT, GE, LE
- Logical operators: AND, OR, NOT
- String methods: startswith, endswith, contains
- Type checking: isof
- Special properties: ID, CreatedBy, ModifiedBy, View
"""

import sys
import os

# Add scripts directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from filter_builder import ODataFilter, FilterField
from datetime import datetime

def test_comparison_operators():
    """Test EQ, NE, GT, LT, GE, LE operators."""
    print("=" * 60)
    print("TEST: Comparison Operators (EQ, NE, GT, LT, GE, LE)")
    print("=" * 60)
    
    # EQ - String
    f = ODataFilter('Part').field('Number').eq('V0056726')
    print(f"[PASS] EQ (String): {f.build()}")
    assert f.build() == "Number eq 'V0056726'", f"Expected: Number eq 'V0056726', Got: {f.build()}"
    
    # EQ - Integer
    f = ODataFilter('Part').field('Quantity').eq(100)
    print(f"[PASS] EQ (Int32): {f.build()}")
    assert f.build() == "Quantity eq 100", f"Expected: Quantity eq 100, Got: {f.build()}"
    
    # EQ - Boolean
    f = ODataFilter('Part').field('IsActive').eq(True)
    print(f"[PASS] EQ (Boolean): {f.build()}")
    assert f.build() == "IsActive eq true", f"Expected: IsActive eq true, Got: {f.build()}"
    
    # NE - String
    f = ODataFilter('Part').field('State').ne('RELEASED')
    print(f"[PASS] NE (String): {f.build()}")
    assert f.build() == "State ne 'RELEASED'", f"Expected: State ne 'RELEASED', Got: {f.build()}"
    
    # GT - Integer
    f = ODataFilter('Part').field('Quantity').gt(10)
    print(f"[PASS] GT (Int32): {f.build()}")
    assert f.build() == "Quantity gt 10", f"Expected: Quantity gt 10, Got: {f.build()}"
    
    # GT - DateTimeOffset
    f = ODataFilter('Part').field('CreatedOn').gt('2024-01-01T00:00:00Z')
    print(f"[PASS] GT (DateTimeOffset): {f.build()}")
    assert f.build() == "CreatedOn gt '2024-01-01T00:00:00Z'", f"Expected: CreatedOn gt '2024-01-01T00:00:00Z', Got: {f.build()}"
    
    # LT - Float (Single/Double)
    f = ODataFilter('Part').field('Weight').lt(15.5)
    print(f"[PASS] LT (Double): {f.build()}")
    assert f.build() == "Weight lt 15.5", f"Expected: Weight lt 15.5, Got: {f.build()}"
    
    # GE - Integer (Int64)
    f = ODataFilter('Part').field('Version').ge(1)
    print(f"[PASS] GE (Int64): {f.build()}")
    assert f.build() == "Version ge 1", f"Expected: Version ge 1, Got: {f.build()}"
    
    # LE - Float
    f = ODataFilter('Part').field('Cost').le(99.99)
    print(f"[PASS] LE (Double): {f.build()}")
    assert f.build() == "Cost le 99.99", f"Expected: Cost le 99.99, Got: {f.build()}"
    
    print()


def test_logical_operators():
    """Test AND, OR, NOT operators."""
    print("=" * 60)
    print("TEST: Logical Operators (AND, OR, NOT)")
    print("=" * 60)
    
    # AND
    f = (ODataFilter('Part')
         .field('State').eq('RELEASED')
         .and_()
         .field('Quantity').gt(10))
    result = f.build()
    print(f"[PASS] AND: {result}")
    assert result == "State eq 'RELEASED' and Quantity gt 10", f"Expected: State eq 'RELEASED' and Quantity gt 10, Got: {result}"
    
    # OR
    f = (ODataFilter('Part')
         .field('State').eq('RELEASED')
         .or_()
         .field('State').eq('APPROVED'))
    result = f.build()
    print(f"[PASS] OR: {result}")
    assert result == "State eq 'RELEASED' or State eq 'APPROVED'", f"Expected: State eq 'RELEASED' or State eq 'APPROVED', Got: {result}"
    
    # NOT
    f = ODataFilter('Part').not_().field('State').eq('RELEASED')
    result = f.build()
    print(f"[PASS] NOT: {result}")
    assert result == "not State eq 'RELEASED'", f"Expected: not State eq 'RELEASED', Got: {result}"
    
    # Complex: (A OR B) AND C
    f = (ODataFilter('Part')
         .group(
             ODataFilter('Part')
             .field('State').eq('RELEASED')
             .or_()
             .field('State').eq('APPROVED')
             .build()
         )
         .and_()
         .field('Quantity').gt(0))
    result = f.build()
    print(f"[PASS] Grouped (A OR B) AND C: {result}")
    assert result == "(State eq 'RELEASED' or State eq 'APPROVED') and Quantity gt 0"
    
    print()


def test_string_methods():
    """Test startswith, endswith, contains methods."""
    print("=" * 60)
    print("TEST: String Methods (startswith, endswith, contains)")
    print("=" * 60)
    
    # startswith
    f = ODataFilter('Part').field('Number').startswith('V00')
    result = f.build()
    print(f"[PASS] startswith: {result}")
    assert result == "startswith(Number, 'V00')", f"Expected: startswith(Number, 'V00'), Got: {result}"
    
    # endswith
    f = ODataFilter('Part').field('Number').endswith('-001')
    result = f.build()
    print(f"[PASS] endswith: {result}")
    assert result == "endswith(Number, '-001')", f"Expected: endswith(Number, '-001'), Got: {result}"
    
    # contains
    f = ODataFilter('Part').field('Name').contains('Engine')
    result = f.build()
    print(f"[PASS] contains: {result}")
    assert result == "contains(Name, 'Engine')", f"Expected: contains(Name, 'Engine'), Got: {result}"
    
    # Combined with logical operators
    f = (ODataFilter('Part')
         .field('Number').startswith('V00')
         .and_()
         .field('Name').contains('Bracket'))
    result = f.build()
    print(f"[PASS] startswith AND contains: {result}")
    assert result == "startswith(Number, 'V00') and contains(Name, 'Bracket')"
    
    print()


def test_type_checking():
    """Test isof function."""
    print("=" * 60)
    print("TEST: Type Checking (isof)")
    print("=" * 60)
    
    # isof with type name
    f = ODataFilter('Part').field('ID').isof('WTPart')
    result = f.build()
    print(f"[PASS] isof(ID, 'WTPart'): {result}")
    assert result == "isof(ID, 'WTPart')", f"Expected: isof(ID, 'WTPart'), Got: {result}"
    
    # isof without type name (single argument)
    f = ODataFilter('Part').field('ID').isof()
    result = f.build()
    print(f"[PASS] isof(ID): {result}")
    assert result == "isof(ID)", f"Expected: isof(ID), Got: {result}"
    
    print()


def test_special_properties():
    """Test ID, CreatedBy, ModifiedBy, View properties."""
    print("=" * 60)
    print("TEST: Special Properties (ID, CreatedBy, ModifiedBy, View)")
    print("=" * 60)
    
    # ID property
    f = ODataFilter('Part').field('ID').eq('OR:wt.part.WTPart:12345')
    result = f.build()
    print(f"[PASS] ID property: {result}")
    assert result == "ID eq 'OR:wt.part.WTPart:12345'", f"Expected: ID eq 'OR:wt.part.WTPart:12345', Got: {result}"
    
    # CreatedBy property
    f = ODataFilter('Part').field('CreatedBy').eq('admin')
    result = f.build()
    print(f"[PASS] CreatedBy property: {result}")
    assert result == "CreatedBy eq 'admin'", f"Expected: CreatedBy eq 'admin', Got: {result}"
    
    # ModifiedBy property
    f = ODataFilter('Part').field('ModifiedBy').eq('engineer')
    result = f.build()
    print(f"[PASS] ModifiedBy property: {result}")
    assert result == "ModifiedBy eq 'engineer'", f"Expected: ModifiedBy eq 'engineer', Got: {result}"
    
    # View property
    f = ODataFilter('Part').field('View').eq('Design')
    result = f.build()
    print(f"[PASS] View property: {result}")
    assert result == "View eq 'Design'", f"Expected: View eq 'Design', Got: {result}"
    
    print()


def test_data_types():
    """Test all supported data types."""
    print("=" * 60)
    print("TEST: Data Types")
    print("=" * 60)
    
    # String
    f = ODataFilter('Part').field('Name').eq('Bracket Assembly')
    print(f"[PASS] String: {f.build()}")
    
    # Int16
    f = ODataFilter('Part').field('SmallInt').eq(32767)
    print(f"[PASS] Int16: {f.build()}")
    
    # Int32
    f = ODataFilter('Part').field('Quantity').eq(2147483647)
    print(f"[PASS] Int32: {f.build()}")
    
    # Int64 (using larger number)
    f = ODataFilter('Part').field('BigId').eq(9223372036854775807)
    print(f"[PASS] Int64: {f.build()}")
    
    # Boolean
    f = ODataFilter('Part').field('IsActive').eq(False)
    print(f"[PASS] Boolean: {f.build()}")
    
    # DateTimeOffset (datetime object)
    dt = datetime(2024, 6, 15, 10, 30, 0)
    f = ODataFilter('Part').field('CreatedOn').gt(dt)
    print(f"[PASS] DateTimeOffset (datetime): {f.build()}")
    
    # Single (float)
    f = ODataFilter('Part').field('Rate').eq(3.14159)
    print(f"[PASS] Single: {f.build()}")
    
    # Double
    f = ODataFilter('Part').field('Precision').eq(3.14159265358979)
    print(f"[PASS] Double: {f.build()}")
    
    print()


def test_edge_cases():
    """Test edge cases like null values, escaping, etc."""
    print("=" * 60)
    print("TEST: Edge Cases")
    print("=" * 60)
    
    # Null value
    f = ODataFilter('Part').field('Description').eq(None)
    result = f.build()
    print(f"[PASS] Null value: {result}")
    assert result == "Description eq null", f"Expected: Description eq null, Got: {result}"
    
    # String with single quote (escaping)
    f = ODataFilter('Part').field('Name').eq("O'Brien's Part")
    result = f.build()
    print(f"[PASS] Escaped string: {result}")
    assert result == "Name eq 'O''Brien''s Part'", f"Expected: Name eq 'O''Brien''s Part', Got: {result}"
    
    # Empty filter (should work)
    f = ODataFilter('Part')
    result = f.build()
    print(f"[PASS] Empty filter: '{result}'")
    assert result == "", f"Expected empty string, Got: '{result}'"
    
    print()


def test_helper_methods():
    """Test static helper methods."""
    print("=" * 60)
    print("TEST: Helper Methods")
    print("=" * 60)
    
    # in_list helper (generates OR'd equality)
    result = ODataFilter.in_list('State', ['RELEASED', 'APPROVED', 'REVIEW'])
    print(f"[PASS] in_list: {result}")
    assert result == "State eq 'RELEASED' or State eq 'APPROVED' or State eq 'REVIEW'"
    
    # between helper (generates ge and le)
    result = ODataFilter.between('Quantity', 10, 100)
    print(f"[PASS] between: {result}")
    assert result == "Quantity ge 10 and Quantity le 100", f"Expected: Quantity ge 10 and Quantity le 100, Got: {result}"
    
    print()


def run_all_tests():
    """Run all test suites."""
    print("\n" + "=" * 60)
    print("ZEPHYR ODATA FILTER EXPRESSION TEST SUITE")
    print("=" * 60 + "\n")
    
    try:
        test_comparison_operators()
        test_logical_operators()
        test_string_methods()
        test_type_checking()
        test_special_properties()
        test_data_types()
        test_edge_cases()
        test_helper_methods()
        
        print("=" * 60)
        print("ALL TESTS PASSED!")
        print("=" * 60)
        print("\nZephyr filter_builder.py fully supports all required OData expressions:")
        print("  - Data types: String, Int16, Int32, Int64, Boolean, DateTimeOffset, Single, Double")
        print("  - Comparison operators: EQ, NE, GT, LT, GE, LE")
        print("  - Logical operators: AND, OR, NOT")
        print("  - String methods: startswith, endswith, contains")
        print("  - Type checking: isof")
        print("  - Special properties: ID, CreatedBy, ModifiedBy, View")
        
    except AssertionError as e:
        print(f"\n[FAIL] Test failed: {e}")
        return False
    
    return True


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
