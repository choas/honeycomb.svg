import math
import sys
from typing import List, Tuple

def generate_honeycomb_svg(columns: int, rows: int, length: float, angle: float, distance: float) -> str:
    """
    Generate an SVG file with a honeycomb pattern rotated 90 degrees.
    
    Args:
        columns: Number of columns per row
        rows: Number of rows (includes odd and even rows)
        length: Length of each side of the honeycomb in mm
        angle: Angle between the left and right sides of the honeycomb in degrees
        distance: Distance between each honeycomb in mm
        
    Returns:
        SVG content as a string
    """
    # Calculate geometric properties
    # Convert angle to radians
    angle_rad = math.radians(angle)
    
    # Calculate height and width of a single honeycomb (rotated 90 degrees)
    inner_angle = (180 - angle) / 2
    inner_angle_rad = math.radians(inner_angle)
    
    # For the 90-degree rotated honeycomb:
    # Width becomes the vertical dimension of the original
    # Height becomes the horizontal dimension of the original
    w = 2 * length * math.sin(inner_angle_rad)  # Now this is the horizontal dimension
    h = 2 * length * math.cos(inner_angle_rad) + length  # Now this is the vertical dimension
    
    # Calculate the horizontal offset for even columns
    offset_y = w / 2 + distance / 2
    
    # Calculate the vertical offset between columns
    offset_x = h + distance
    
    # Calculate the vertical spacing between honeycombs in the same column
    spacing_y = w + distance
    
    # Calculate the total width and height of the SVG
    total_width = columns * offset_x / 2 + h / 2
    total_height = rows * spacing_y + offset_y
    
    # Start generating SVG
    svg = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg width="{total_width}mm" height="{total_height}mm" viewBox="0 0 {total_width} {total_height}"
     xmlns="http://www.w3.org/2000/svg">
  <title>Honeycomb Pattern (90° Rotation)</title>
  <desc>Generated honeycomb pattern with {columns} columns and {rows} rows, rotated 90 degrees</desc>
"""
    
    # Generate honeycomb cells
    for col in range(columns):
        is_even_col = col % 2 == 1
        # Adjust the number of rows for even columns if needed
        row_count = rows - 1 if is_even_col else rows
        
        for row in range(row_count):
            # Calculate cell position
            y = row * spacing_y
            if is_even_col:
                y += offset_y
            x = col * offset_x / 2
            
            # Generate points for the honeycomb
            points = calculate_honeycomb_points(x, y, length, angle)
            
            # Add the hexagon to the SVG
            points_str = " ".join([f"{x},{y}" for x, y in points])
            svg += f'  <polygon points="{points_str}" fill="none" stroke="black" stroke-width="0.5"/>\n'
    
    # Close the SVG
    svg += "</svg>"
    
    return svg

def calculate_honeycomb_points(x: float, y: float, length: float, angle: float) -> List[Tuple[float, float]]:
    """
    Calculate the six points of a honeycomb rotated 90 degrees.
    
    Args:
        x: X-coordinate of the left-middle point of the honeycomb
        y: Y-coordinate of the left-middle point of the honeycomb
        length: Length of each side of the honeycomb
        angle: Angle between the left and right sides in degrees
        
    Returns:
        List of (x, y) tuples representing the six corners of the honeycomb
    """
    # Calculate geometry
    inner_angle = (180 - angle) / 2
    inner_angle_rad = math.radians(inner_angle)
    
    # Calculate the offset for vertical sides
    dx = length * math.sin(inner_angle_rad)
    dy = length * math.cos(inner_angle_rad)
    
    # Calculate the six points for a 90-degree rotated honeycomb
    points = [
        (x, y),  # Left-middle
        (x + dx, y - dy),  # Top-left
        (x + dx + length, y - dy),  # Top-right
        (x + 2 * dx + length, y),  # Right-middle
        (x + dx + length, y + dy),  # Bottom-right
        (x + dx, y + dy),  # Bottom-left
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
    filename = f"honeycomb_rotated_c{columns}_r{rows}_l{length}_a{angle}_d{distance}.svg"
    save_svg_to_file(svg_content, filename)
    print(f"SVG file saved as {filename}")

if __name__ == "__main__":
    main()
