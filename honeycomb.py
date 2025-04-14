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
        angle: Angle between the top and bottom sides of the honeycomb in degrees
        distance: Distance between each honeycomb in mm
        
    Returns:
        SVG content as a string
    """
    # Calculate geometric properties
    # Convert angle to radians
    angle_rad = math.radians(angle)
    
    # Calculate height and width of a single honeycomb
    # For a regular hexagon, height is 2 * length * sin(60°)
    # For a non-regular hexagon, we need to adjust based on the provided angle
    inner_angle = (180 - angle) / 2
    inner_angle_rad = math.radians(inner_angle)
    
    # Calculate the height of the honeycomb (vertical distance)
    h = 2 * length * math.sin(inner_angle_rad)
    
    # Calculate the width of the honeycomb
    w = 2 * length * math.cos(inner_angle_rad) + length
    
    # Calculate the horizontal offset for even rows
    offset_x = w / 2 + distance / 2
    
    # Calculate the vertical offset between rows
    offset_y = h + distance
    
    # Calculate the horizontal spacing between honeycombs in the same row
    spacing_x = w + distance
    
    # Calculate the total width and height of the SVG
    total_width = columns * spacing_x + offset_x
    total_height = rows * offset_y / 2 + h / 2
    
    # Start generating SVG
    svg = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg width="{total_width}mm" height="{total_height}mm" viewBox="0 0 {total_width} {total_height}"
     xmlns="http://www.w3.org/2000/svg">
  <title>Honeycomb Pattern</title>
  <desc>Generated honeycomb pattern with {columns} columns and {rows} rows</desc>
"""
    
    # Generate honeycomb cells
    for row in range(rows):
        is_even_row = row % 2 == 1
        # Adjust the number of columns for even rows if needed
        cols = columns - 1 if is_even_row else columns
        
        for col in range(cols):
            # Calculate cell position
            x = col * spacing_x
            if is_even_row:
                x += offset_x
            y = row * offset_y / 2
            
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
    Calculate the six points of a honeycomb.
    
    Args:
        x: X-coordinate of the top-left point of the honeycomb
        y: Y-coordinate of the top-left point of the honeycomb
        length: Length of each side of the honeycomb
        angle: Angle between the top and bottom sides in degrees
        
    Returns:
        List of (x, y) tuples representing the six corners of the honeycomb
    """
    # Calculate geometry
    inner_angle = (180 - angle) / 2
    inner_angle_rad = math.radians(inner_angle)
    
    # Calculate the offset for horizontal sides
    dx = length * math.cos(inner_angle_rad)
    dy = length * math.sin(inner_angle_rad)
    
    # Calculate the six points
    points = [
        (x, y),  # Top-left
        (x + length, y),  # Top-right
        (x + length + dx, y + dy),  # Right
        (x + length, y + 2 * dy),  # Bottom-right
        (x, y + 2 * dy),  # Bottom-left
        (x - dx, y + dy),  # Left
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
