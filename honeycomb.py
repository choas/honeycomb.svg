import math
import sys
from typing import List, Tuple

def generate_honeycomb_svg(columns: int, rows: int, length: float, angle: float, distance: float) -> str:
    """
    Generate an SVG file with a honeycomb pattern.
    
    Args:
        columns: Number of columns per row
        rows: Number of rows (includes odd and even rows)
        length: Length of each side of the honeycomb in mm
        angle: Angle between the top sides of the honeycomb in degrees
        distance: Distance between each honeycomb in mm
        
    Returns:
        SVG content as a string
    """
    # Calculate geometric properties of a single hexagon cell
    
    # The angle between the top sides
    internal_angle = angle
    
    # Calculate angle for the side relative to horizontal
    alpha = (180 - internal_angle) / 2
    alpha_rad = math.radians(alpha)
    
    # Calculate width and height of a single hexagon
    # Height calculation: from top point to bottom point
    hexagon_height = 2 * length * math.sin(alpha_rad) + length
    
    # Width calculation: from leftmost to rightmost point
    hexagon_width = 2 * length * math.cos(alpha_rad)
    
    # Calculate step sizes between cells
    # Horizontal distance between centers of hexagons in the same row
    x_step = hexagon_width + distance
    
    # Vertical distance between rows
    y_step = length + length * math.sin(alpha_rad) + distance/2
    
    # Offset for odd/even rows
    x_offset = x_step / 2
    
    # Calculate SVG dimensions
    total_width = columns * x_step + x_offset
    total_height = rows * y_step + length * math.sin(alpha_rad)
    
    # Start generating SVG
    svg = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg width="{total_width}mm" height="{total_height}mm" viewBox="0 0 {total_width} {total_height}"
     xmlns="http://www.w3.org/2000/svg">
  <title>Honeycomb Pattern</title>
  <desc>Generated honeycomb pattern with {columns} columns and {rows} rows</desc>
"""
    
    # Generate honeycomb cells
    for row in range(rows):
        is_odd_row = row % 2 == 1
        
        # Set number of columns for this row (may be fewer for odd rows)
        row_columns = columns if not is_odd_row else columns - 1
        
        for col in range(row_columns):
            # Calculate center position of this hexagon
            x = col * x_step
            if is_odd_row:
                x += x_offset
            y = row * y_step
            
            # Generate points for this hexagon
            points = calculate_hexagon(x, y, length, internal_angle)
            
            # Add hexagon to SVG
            points_str = " ".join([f"{x},{y}" for x, y in points])
            svg += f'  <polygon points="{points_str}" fill="none" stroke="black" stroke-width="0.5"/>\n'
    
    # Close the SVG
    svg += "</svg>"
    
    return svg

def calculate_hexagon(x: float, y: float, side_length: float, top_angle: float) -> List[Tuple[float, float]]:
    """
    Calculate the six points of a hexagon with top-center at (x, y).
    All sides have equal length = side_length.
    The angle between the two top sides = top_angle.
    
    Args:
        x: X-coordinate of the top-center point
        y: Y-coordinate of the top-center point
        side_length: Length of each side of the hexagon
        top_angle: Angle between the two top sides in degrees
        
    Returns:
        List of (x, y) tuples representing the six corners of the hexagon
    """
    # Calculate half of the top angle
    half_angle = (180 - top_angle) / 2
    half_angle_rad = math.radians(half_angle)
    
    # Calculate horizontal and vertical components of the sides
    dx = side_length * math.cos(half_angle_rad)
    dy = side_length * math.sin(half_angle_rad)
    
    # Calculate the six vertices
    # Starting from top-left, going clockwise
    points = [
        (x - dx, y + dy),                    # Top-left
        (x + dx, y + dy),                    # Top-right
        (x + dx + side_length, y + dy * 2),  # Right
        (x + dx, y + dy * 2 + side_length),  # Bottom-right
        (x - dx, y + dy * 2 + side_length),  # Bottom-left
        (x - dx - side_length, y + dy * 2)   # Left
    ]
    
    return points

def save_svg_to_file(svg_content: str, filename: str) -> None:
    """Save SVG content to a file."""
    with open(filename, 'w') as f:
        f.write(svg_content)

def main():
    # Default parameters
    columns = 10
    rows = 8
    length = 50
    angle = 120
    distance = 2
    
    # Parse command line arguments if provided
    if len(sys.argv) > 1:
        try:
            columns = int(sys.argv[1])
            rows = int(sys.argv[2])
            length = float(sys.argv[3])
            angle = float(sys.argv[4])
            distance = float(sys.argv[5])
        except (IndexError, ValueError):
            print("Usage: python honeycomb.py [columns rows length angle distance]")
            print("Using default values instead.")
    
    # Generate SVG
    svg_content = generate_honeycomb_svg(columns, rows, length, angle, distance)
    
    # Save to file
    filename = f"honeycomb_c{columns}_r{rows}_l{length}_a{angle}_d{distance}.svg"
    save_svg_to_file(svg_content, filename)
    print(f"SVG file saved as {filename}")

if __name__ == "__main__":
    main()
