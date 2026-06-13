# Summary of Code

## Structure

- **points.py**: Contains a `Point2D` class representing 2D points with x and y coordinates.
- **force_directed_graph.py**: Contains a `ForceDirectedGraph` class handling force-directed graph visualization using GTK for rendering.

## Assumptions

- The code assumes the existence of:
  - A `graph` object with methods `nodes()` and `edges()`.
  - A `graphical_event_manager` (GEM) with attributes like `display_node_labels`, `b1_down`, etc.
  - Constants such as `SPRING_CONSTANT`, `EQUILIBRIUM_DISPLACEMENT`, `FRICTION`, `TIME_STEP`, `W_0`, `H_0`, and `W_1`, `H_1`.

## Dependencies

- **External Libraries**:
  - `math`: For mathematical operations.
  - `gtk`: For graphical rendering (GTK library).
  - `points.Point2D`: For point representation.

- **Internal Modules**:
  - `constants`: Contains various constants used in the graph calculations and rendering.

## Behaviour

- **Initialization**: The `ForceDirectedGraph` class is initialized with a graph object and a graphical event manager.
- **Translation Methods**:
  - `translate(x0, y0, w0, h0, w1, h1)`: Translates coordinates from one canvas size to another.
  - `reverse(x1, y1, w0, h0, w1, h1)`: Reverses the translation process.
- **Drawing**:
  - `draw_to_pixmap(pixmap, gc, style, node_label_vert_spacing)`: Renders the graph onto a pixmap.
- **Force Calculations**:
  - `net_electrostatic_force_at_node(tag_A)`: Calculates net electrostatic forces at a node.
  - `net_spring_force_at_node(tag)`: Calculates net spring forces at a node.
  - `net_force_at_node(tag)`: Combines electrostatic and spring forces to get the net force.
- **Velocity and Displacement**:
  - `velocity_at_tag(tag)`: Updates velocity based on net force.
  - `displacement_at_node(tag)`: Calculates displacement based on net force (NOTE: Velocity is not used).
- **Iteration**:
  - `iterate(pixmap, gc, style, node_label_vertical_spacing)`: Iterates through nodes to update positions and redraw the graph.

## Bugs

- **Velocity Ignored**: Displacement calculations do not use velocity.
- **Inconsistent Force Calculation**: The net force calculation does not seem to be correctly implemented, as it recalculates forces multiple times without caching intermediate results.

## Potential Issues

- **Performance**: Repeatedly calculating forces and displacements for each node can lead to performance issues in large graphs.
- **Code Duplication**: Force calculations are repeated multiple times (electrostatic, spring, net force) which can be optimized by caching results.
- **Error Handling**: Minimal error handling is present, especially around division by zero and invalid input scenarios.
- **Graphical Dependencies**: The code heavily depends on GTK for rendering, making it less portable to other graphical libraries.