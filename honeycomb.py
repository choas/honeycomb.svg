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
    # Calculate geometric properties
    inner_angle = (180 - angle) / 2
    inner_angle_rad = math.radians(inner_angle)
    
    # Calculate dimensions of a single honeycomb
    hex_height = length * (1 + 2 * math.sin(inner_angle_rad))
    hex_width = 2 * length * math.cos(inner_angle_rad)
    
    # Calculate offsets for positioning
    # Horizontal distance between centers of adjacent hexagons in the same row
    x_step = hex_width + distance
    
    # Vertical distance between centers of adjacent rows
    y_step = 0.75 * hex_height + distance / 2
    
    # Horizontal offset for even rows
    x_offset = x_step / 2
    
    # Calculate total SVG dimensions
    total_width = columns * x_step + x_offset
    total_height = rows * y_step + 0.25 * hex_height
    
    # Start generating SVG
    svg = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg width="{total_width}mm" height="{total_height}mm" viewBox="0 0 {total_width} {total_height}"
     xmlns="http://www.w3.org/2000/svg">
  <title>Honeycomb Pattern</title>
  <desc>Generated honeycomb pattern with {columns} columns and {rows} rows</desc>
"""
    
    # Generate honeycomb cells
    for row in range(rows):
        # Determine if this is an even row (0-indexed)
        is_even_row = row % 2 == 0
        
        for col in range(columns):
            # Calculate cell center position
            x_center = col * x_step
            if not is_even_row:
                x_center += x_offset
            y_center = row * y_step
            
            # Generate points for the honeycomb
            points = calculate_honeycomb_points(x_center, y_center, length, angle)
            
            # Add the hexagon to the SVG
            points_str = " ".join([f"{x},{y}" for x, y in points])
            svg += f'  <polygon points="{points_str}" fill="none" stroke="black" stroke-width="0.5"/>\n'
    
    # Close the SVG
    svg += "</svg>"
    
    return svg

def calculate_honeycomb_points(x_center: float, y_center: float, length: float, angle: float) -> List[Tuple[float, float]]:
    """
    Calculate the six points of a honeycomb with the center at (x_center, y_center).
    
    Args:
        x_center: X-coordinate of the center point of the honeycomb
        y_center: Y-coordinate of the center point of the honeycomb
        length: Length of each side of the honeycomb
        angle: Angle between the top sides in degrees
        
    Returns:
        List of (x, y) tuples representing the six corners of the honeycomb
    """
    # Calculate geometry
    inner_angle = (180 - angle) / 2
    inner_angle_rad = math.radians(inner_angle)
    
    # Calculate the dimensions
    h = length * math.sin(inner_angle_rad)
    w = length * math.cos(inner_angle_rad)
    
    # Calculate the six points around the center
    points = [
        (x_center - w, y_center - h),           # Top-left
        (x_center + w, y_center - h),           # Top-right
        (x_center + length, y_center),          # Right
        (x_center + w, y_center + h),           # Bottom-right
        (x_center - w, y_center + h),           # Bottom-left
        (x_center - length, y_center),          # Left
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
