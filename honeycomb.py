import math
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def generate_honeycomb_svg(columns=10, rows=8, length=50, angle=120, distance=2, filename="honeycomb.svg"):
    """
    Generate an SVG file with a honeycomb pattern.
    
    Args:
        columns: Number of columns per row
        rows: Total number of rows (includes odd and even rows)
        length: Length of each side of a honeycomb in mm
        angle: Angle between the top and bottom tips of the honeycomb in degrees
        distance: Distance between honeycombs in mm
        filename: Output SVG filename
    """
    # Calculate dimensions of a single honeycomb
    angle_rad = math.radians(angle)
    # Height of the hexagon from top to bottom
    height = length * (1 + 2 * math.sin(math.radians(90 - angle/2)))
    # Width of the hexagon from side to side
    width = 2 * length * math.cos(math.radians(90 - angle/2))
    
    logger.info(f"Honeycomb dimensions - Width: {width:.2f}mm, Height: {height:.2f}mm")
    
    # Calculate horizontal and vertical spacing between honeycombs
    h_spacing = width + distance
    v_spacing = height * 3/4 + distance
    
    # Calculate the offset for odd rows
    odd_row_offset = width / 2
    
    # Check if the odd_row_offset and distance are compatible
    min_offset = width/2
    if odd_row_offset < min_offset:
        logger.info(f"Adjusting odd row offset from {odd_row_offset:.2f} to minimum {min_offset:.2f}")
        odd_row_offset = min_offset
    
    # Verify spacing is sufficient to prevent overlapping
    min_v_spacing = height/2 + distance
    if v_spacing < min_v_spacing:
        logger.info(f"Adjusting vertical spacing from {v_spacing:.2f} to minimum {min_v_spacing:.2f}")
        v_spacing = min_v_spacing
    
    # Calculate total SVG dimensions
    total_width = (columns - 0.5) * h_spacing + distance
    total_height = rows * v_spacing + height/4 + distance
    
    logger.info(f"Total SVG dimensions - Width: {total_width:.2f}mm, Height: {total_height:.2f}mm")
    
    # Start creating the SVG
    svg = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg width="{total_width}mm" height="{total_height}mm" viewBox="0 0 {total_width} {total_height}"
     xmlns="http://www.w3.org/2000/svg">
  <title>Honeycomb Pattern</title>
  <desc>Generated honeycomb pattern with {columns} columns and {rows} rows</desc>
  <style>
    .hexagon {{
      fill: none;
      stroke: black;
      stroke-width: 1;
    }}
  </style>
"""
    
    # Generate each honeycomb
    for row in range(rows):
        # Calculate row offset (odd rows are shifted)
        row_offset = odd_row_offset if row % 2 == 1 else 0
        
        # Determine actual number of columns for this row
        actual_columns = columns - 1 if row % 2 == 1 else columns
        
        for col in range(actual_columns):
            x_center = col * h_spacing + row_offset + distance + width/2
            y_center = row * v_spacing + distance + height/2
            
            # Generate hexagon points
            points = []
            for i in range(6):
                # Angle for each vertex (starting from the right and going counter-clockwise)
                theta = math.radians(60 * i - 30)
                x = x_center + length * math.cos(theta)
                y = y_center + length * math.sin(theta)
                points.append(f"{x:.2f},{y:.2f}")
            
            # Add hexagon to SVG
            svg += f'  <polygon class="hexagon" points="{" ".join(points)}" />\n'
    
    # Close SVG
    svg += "</svg>"
    
    # Write SVG to file
    with open(filename, 'w') as f:
        f.write(svg)
    
    logger.info(f"SVG file '{filename}' has been created successfully.")
    return svg

if __name__ == "__main__":
    # Use the parameters provided in the problem
    generate_honeycomb_svg(
        columns=10,
        rows=8,
        length=50,
        angle=120,
        distance=2,
        filename="honeycomb.svg"
    )

