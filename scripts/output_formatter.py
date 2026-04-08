#!/usr/bin/env python3
"""Output Formatter for Windchill PLM scripts.

Provides formatted output for Telegram gateway with:
- Markdown tables
- Bold headers
- Emoji indicators
- Code blocks for IDs
- Truncation for long content

Usage:
    from output_formatter import OutputFormatter
    
    formatter = OutputFormatter()
    formatter.print_header("Query Results")
    formatter.print_entity_table(entities, "Part", ["ID", "Name", "Number", "State"])
    formatter.print_success(f"Found {len(entities)} items")
"""

import os
import sys
import json
from datetime import datetime
from typing import List, Dict, Any, Optional


class OutputFormatter:
    """Format output for Telegram gateway with Markdown support."""
    
    # Emoji indicators
    EMOJI = {
        'success': '✅',
        'error': '❌',
        'warning': '⚠️',
        'info': 'ℹ️',
        'document': '📄',
        'part': '🔧',
        'supplier': '🏭',
        'change': '📝',
        'quality': '🔍',
        'user': '👤',
        'folder': '📁',
        'container': '📦',
        'bom': '📊',
        'workflow': '🔄',
        'cad': '📐',
        'process': '⚙️',
        'customer': '💬',
        'caps': '🔑',
        'chart': '📈',
        'clock': '🕐',
        'link': '🔗',
        'bullet': '•',
        'arrow': '→',
        'check': '☑️',
        'cross': '☒',
    }
    
    # Entity type to emoji mapping
    ENTITY_EMOJI = {
        'Document': '📄',
        'Part': '🔧',
        'Supplier': '🏭',
        'ChangeNotice': '📝',
        'ChangeRequest': '📝',
        'ChangeTask': '📝',
        'QualityAction': '🔍',
        'NonConformance': '⚠️',
        'CAPA': '🎯',
        'User': '👤',
        'Group': '👥',
        'Organization': '🏢',
        'Folder': '📁',
        'Container': '📦',
        'ProductContainer': '📦',
        'LibraryContainer': '📚',
        'BOM': '📊',
        'Workflow': '🔄',
        'CADDocument': '📐',
        'ProcessPlan': '⚙️',
        'CustomerExperience': '💬',
        'Place': '📍',
        'Subject': '🏷️',
        'QualityContact': '📞',
    }
    
    # Max lengths for truncation
    MAX_NAME_LENGTH = 40
    MAX_DESC_LENGTH = 50
    MAX_TABLE_ROWS = 20
    MAX_DETAIL_ITEMS = 15
    
    def __init__(self, output_format: str = "markdown"):
        """
        Initialize formatter.
        
        Args:
            output_format: "markdown" (default) or "text"
        """
        self.output_format = output_format
        self._buffer = []
    
    def _add(self, text: str):
        """Add text to buffer."""
        self._buffer.append(text)
    
    def _flush(self):
        """Flush buffer to stdout."""
        output = '\n'.join(self._buffer)
        self._buffer = []
        print(output)
    
    def _truncate(self, text: str, max_len: int) -> str:
        """Truncate text if too long."""
        if not text:
            return 'N/A'
        text = str(text)
        if len(text) <= max_len:
            return text
        return text[:max_len-3] + '...'
    
    def _format_value(self, value: Any, max_len: int = None) -> str:
        """Format a value for display."""
        if value is None:
            return 'N/A'
        if isinstance(value, dict):
            # Handle State objects
            if 'Display' in value:
                return value['Display']
            if 'Value' in value:
                return value['Value']
            return json.dumps(value, indent=0)[:50]
        if isinstance(value, list):
            return f"{len(value)} items"
        text = str(value)
        if max_len:
            text = self._truncate(text, max_len)
        return text
    
    def _format_state(self, state: Any) -> str:
        """Format state with color indicator."""
        value = self._format_value(state)
        # Add state indicator
        state_indicators = {
            'RELEASED': '🟢',
            'APPROVED': '🟢',
            'INWORK': '🔵',
            'IN_WORK': '🔵',
            'REVIEW': '🟡',
            'OPEN': '🟡',
            'CANCELLED': '⚫',
            'REJECTED': '🔴',
            'CLOSED': '⚫',
        }
        indicator = state_indicators.get(value.upper(), '⚪')
        return f"{indicator} {value}"
    
    # ============================================
    # HEADER METHODS
    # ============================================
    
    def print_header(self, title: str, emoji: str = None):
        """Print a bold header."""
        if emoji is None:
            emoji = self.EMOJI['info']
        self._add(f"\n*{emoji} {title}*\n")
    
    def print_entity_header(self, entity_type: str, count: int = None):
        """Print entity-specific header."""
        emoji = self.ENTITY_EMOJI.get(entity_type, '📋')
        if count is not None:
            self._add(f"\n*{emoji} {entity_type}* `{count} found`\n")
        else:
            self._add(f"\n*{emoji} {entity_type}*\n")
    
    # ============================================
    # STATUS METHODS
    # ============================================
    
    def print_success(self, message: str):
        """Print success message."""
        self._add(f"\n{self.EMOJI['success']} {message}\n")
    
    def print_error(self, message: str, details: str = None):
        """Print error message."""
        self._add(f"\n{self.EMOJI['error']} *ERROR*: {message}")
        if details:
            self._add(f"  `{details}`")
        self._add("")
    
    def print_warning(self, message: str):
        """Print warning message."""
        self._add(f"\n{self.EMOJI['warning']} {message}\n")
    
    def print_info(self, message: str):
        """Print info message."""
        self._add(f"\n{self.EMOJI['info']} {message}\n")
    
    # ============================================
    # TABLE METHODS
    # ============================================
    
    def print_table(self, headers: List[str], rows: List[List[str]], 
                    title: str = None, truncate_rows: int = None):
        """
        Print a Markdown table.
        
        Args:
            headers: Column headers
            rows: Table rows (list of lists)
            title: Optional table title
            truncate_rows: Max rows to display (default: MAX_TABLE_ROWS)
        """
        if not rows:
            self.print_warning("No data to display")
            return
        
        if title:
            self._add(f"\n*{title}*\n")
        
        # Truncate rows if needed
        max_rows = truncate_rows or self.MAX_TABLE_ROWS
        total_rows = len(rows)
        show_truncated = total_rows > max_rows
        rows = rows[:max_rows]
        
        # Calculate column widths
        widths = [len(str(h)) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                if i < len(widths):
                    widths[i] = max(widths[i], len(str(cell)))
        
        # Build header row
        header_row = '| ' + ' | '.join(str(h).ljust(widths[i]) for i, h in enumerate(headers)) + ' |'
        separator = '|' + '|'.join('-' * (w + 2) for w in widths) + '|'
        
        self._add(header_row)
        self._add(separator)
        
        # Build data rows
        for row in rows:
            cells = []
            for i, cell in enumerate(row):
                cell_text = str(cell) if cell is not None else 'N/A'
                if i < len(widths):
                    cell_text = cell_text[:widths[i] + 3]  # Truncate if too long
                cells.append(cell_text)
            row_text = '| ' + ' | '.join(cells[i].ljust(widths[i]) if i < len(widths) else cells[i] 
                                          for i in range(len(cells))) + ' |'
            self._add(row_text)
        
        # Add truncation note
        if show_truncated:
            self._add(f"\n_{self.EMOJI['info']} Showing {max_rows} of {total_rows} rows_")
        
        self._add("")
    
    def print_entity_table(self, entities: List[Dict], entity_type: str, 
                           properties: List[str] = None):
        """
        Print entities as a formatted table.
        
        Args:
            entities: List of entity dictionaries
            entity_type: Type of entity (for display)
            properties: Properties to display (auto-detected if None)
        """
        if not entities:
            self.print_warning(f"No {entity_type}(s) found")
            return
        
        # Auto-detect properties if not provided
        if not properties:
            properties = ['ID', 'Name', 'Number', 'State']
            # Check which properties exist
            sample = entities[0]
            properties = [p for p in properties if p in sample]
        
        # Build header
        emoji = self.ENTITY_EMOJI.get(entity_type, '📋')
        self.print_entity_header(entity_type, len(entities))
        
        # Build rows
        rows = []
        for entity in entities[:self.MAX_TABLE_ROWS]:
            row = []
            for prop in properties:
                value = entity.get(prop)
                if prop.lower() == 'state':
                    value = self._format_state(value)
                else:
                    value = self._format_value(value, 30)
                row.append(value)
            rows.append(row)
        
        self.print_table(properties, rows)
    
    # ============================================
    # DETAIL METHODS
    # ============================================
    
    def print_entity_detail(self, entity: Dict, entity_type: str = "Entity",
                            properties: List[str] = None, exclude: List[str] = None):
        """
        Print detailed entity information.
        
        Args:
            entity: Entity dictionary
            entity_type: Type of entity
            properties: Specific properties to show (None = all)
            exclude: Properties to exclude
        """
        exclude = exclude or ['@odata.context', '@odata.etag', 'AdditionalMetadata']
        
        emoji = self.ENTITY_EMOJI.get(entity_type, '📋')
        name = entity.get('Name', entity.get('Number', 'Unknown'))
        
        self._add(f"\n{emoji} *{entity_type}: {name}*\n")
        
        # Get properties to display
        if properties:
            props = properties
        else:
            props = list(entity.keys())
        
        # Filter and sort properties
        props = [p for p in props if p not in exclude and p in entity]
        
        # Put important properties first
        important = ['ID', 'Number', 'Name', 'State', 'Description']
        props = sorted(props, key=lambda p: (p not in important, props.index(p) if p in props else 999))
        
        for prop in props[:self.MAX_DETAIL_ITEMS]:
            value = entity.get(prop)
            
            # Format based on property type
            if prop.lower() == 'state':
                value = self._format_state(value)
            elif prop.lower() in ['createdon', 'modifiedon', 'date', 'needdate', 'duedate']:
                value = self._format_date(value)
            elif prop == 'ID':
                value = f"`{value}`"
            else:
                value = self._format_value(value)
            
            # Bold property name
            self._add(f"  *{prop}*: {value}")
        
        if len(props) > self.MAX_DETAIL_ITEMS:
            self._add(f"\n  _... and {len(props) - self.MAX_DETAIL_ITEMS} more properties_")
        
        self._add("")
    
    def _format_date(self, date_value: Any) -> str:
        """Format date value."""
        if not date_value:
            return 'N/A'
        try:
            # Parse ISO date
            if 'T' in str(date_value):
                dt = datetime.fromisoformat(str(date_value).replace('Z', '+00:00'))
                return dt.strftime('%Y-%m-%d %H:%M')
            return str(date_value)
        except:
            return str(date_value)
    
    # ============================================
    # LIST METHODS
    # ============================================
    
    def print_list(self, items: List[Any], title: str = None, 
                   bullet: str = None, numbered: bool = False):
        """
        Print a formatted list.
        
        Args:
            items: List items
            title: Optional title
            bullet: Bullet character (default: emoji bullet)
            numbered: Use numbered list
        """
        if not items:
            self.print_warning("No items to display")
            return
        
        if title:
            self._add(f"\n*{title}*\n")
        
        bullet = bullet or self.EMOJI['bullet']
        
        for i, item in enumerate(items[:self.MAX_TABLE_ROWS]):
            prefix = f"{i+1}." if numbered else bullet
            if isinstance(item, dict):
                name = item.get('Name', item.get('Number', str(item)))
                self._add(f" {prefix} {name}")
            else:
                self._add(f" {prefix} {item}")
        
        if len(items) > self.MAX_TABLE_ROWS:
            self._add(f"\n_{self.EMOJI['info']} ... and {len(items) - self.MAX_TABLE_ROWS} more_")
        
        self._add("")
    
    def print_bom_list(self, bom_items: List[Dict], parent_part: str = None):
        """
        Print BOM structure with indentation.
        
        Args:
            bom_items: BOM items with Uses relationship
            parent_part: Parent part number
        """
        if not bom_items:
            self.print_warning("No BOM items found")
            return
        
        self.print_header(f"BOM: {parent_part or 'Part'}", self.EMOJI['bom'])
        
        for item in bom_items[:self.MAX_TABLE_ROWS]:
            part = item.get('Part', {})
            part_name = part.get('Name', 'Unknown')
            part_number = part.get('Number', 'N/A')
            qty = item.get('Quantity', 1)
            
            self._add(f"  {self.EMOJI['bullet']} *{part_number}* - {part_name} `{qty}x`")
        
        self._add("")
    
    # ============================================
    # SUMMARY METHODS
    # ============================================
    
    def print_summary(self, stats: Dict[str, Any]):
        """
        Print operation summary.
        
        Args:
            stats: Dictionary of statistic names and values
        """
        self._add(f"\n{self.EMOJI['chart']} *Summary*\n")
        
        for key, value in stats.items():
            # Format key as title case
            key_formatted = key.replace('_', ' ').title()
            self._add(f"  {self.EMOJI['bullet']} *{key_formatted}*: {value}")
        
        self._add("")
    
    def print_operation_result(self, operation: str, entity_type: str, 
                                entity_name: str, success: bool, 
                                details: str = None):
        """
        Print operation result (create/update/delete).
        
        Args:
            operation: Operation name (Created, Updated, Deleted)
            entity_type: Type of entity
            entity_name: Entity name or number
            success: Whether operation succeeded
            details: Additional details
        """
        if success:
            emoji = self.ENTITY_EMOJI.get(entity_type, '✅')
            self._add(f"\n{self.EMOJI['success']} *{operation}* {emoji} *{entity_type}*: `{entity_name}`")
            if details:
                self._add(f"  {details}")
        else:
            self._add(f"\n{self.EMOJI['error']} *Failed to {operation.lower()}* {entity_type}: `{entity_name}`")
            if details:
                self._add(f"  `{details}`")
        
        self._add("")
    
    # ============================================
    # RAW OUTPUT
    # ============================================
    
    def print_json(self, data: Any, title: str = None):
        """Print JSON data in code block."""
        if title:
            self._add(f"\n*{title}*\n")
        
        json_str = json.dumps(data, indent=2)
        # Truncate if too long
        if len(json_str) > 4000:
            json_str = json_str[:4000] + "\n... (truncated)"
        
        self._add(f"```\n{json_str}\n```")
    
    # ============================================
    # HELPER METHODS
    # ============================================
    
    def print_id(self, oid: str):
        """Format and print Windchill OID."""
        if not oid:
            return "N/A"
        # Extract type and ID from OID
        # Format: OR:com.ptc.domain.EntityType:12345
        return f"`{oid}`"
    
    def print_link(self, url: str, text: str = None):
        """Print a hyperlink."""
        text = text or url
        return f"[{text}]({url})"
    
    def divider(self):
        """Print a divider line."""
        self._add("\n---\n")
    
    def flush(self):
        """Flush buffer and print output."""
        self._flush()


# ============================================
# CONVENIENCE FUNCTIONS
# ============================================

def format_entity(entity: Dict, entity_type: str = None, 
                  properties: List[str] = None) -> str:
    """Format a single entity for display."""
    formatter = OutputFormatter()
    formatter.print_entity_detail(entity, entity_type or "Entity", properties)
    return '\n'.join(formatter._buffer)


def format_table(entities: List[Dict], entity_type: str = None,
                 properties: List[str] = None) -> str:
    """Format entities as a table."""
    formatter = OutputFormatter()
    formatter.print_entity_table(entities, entity_type or "Entity", properties)
    return '\n'.join(formatter._buffer)


# ============================================
# MAIN (for testing)
# ============================================

if __name__ == '__main__':
    # Demo output
    formatter = OutputFormatter()
    
    # Demo header
    formatter.print_header("Windchill PLM Query Results")
    
    # Demo entity table
    demo_parts = [
        {'ID': 'OR:com.ptc.ProdMgmt.Part:12345', 'Name': 'Engine Assembly', 'Number': 'ENG-001', 'State': {'Display': 'RELEASED'}},
        {'ID': 'OR:com.ptc.ProdMgmt.Part:12346', 'Name': 'Piston Component', 'Number': 'PIS-001', 'State': {'Display': 'INWORK'}},
        {'ID': 'OR:com.ptc.ProdMgmt.Part:12347', 'Name': 'Cylinder Head', 'Number': 'CYL-001', 'State': {'Display': 'REVIEW'}},
    ]
    formatter.print_entity_table(demo_parts, "Part")
    
    # Demo entity detail
    formatter.print_entity_detail(demo_parts[0], "Part")
    
    # Demo operation result
    formatter.print_operation_result("Created", "Part", "ENG-001", True, "Part created successfully")
    
    # Demo summary
    formatter.print_summary({
        'total_items': 150,
        'released': 45,
        'in_work': 30,
        'review': 25
    })
    
    formatter.flush()
