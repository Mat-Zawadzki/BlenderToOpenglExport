import bpy
import bmesh
from collections import defaultdict

scale_value = 64

# Function to calculate vertex normals and store unique vertices
def get_unique_vertices_with_normals_and_ibo(obj):
    if obj.type != 'MESH':
        print(f"{obj.name} is not a mesh object.")
        return [], []

    # Create a BMesh from the object
    bm = bmesh.new()
    bm.from_mesh(obj.data)

    # Dictionary to hold unique vertices with normals
    unique_vertices = defaultdict(list)
    index_mapping = {}
    unique_vertex_list = []
    index_buffer = []
    edge_index_buffer = []
    unique_edges = set()
    
    unqi_bits = []
    
    # Iterate through all faces in the mesh
    for face in bm.faces:
        # Get the normal of the face
        face_normal = face.normal

        # Get the material index for the face
        material_index = face.material_index
        material_color = (1.0, 1.0, 1.0)  # Default to white

        # Check if the object has materials
        if obj.data.materials and material_index < len(obj.data.materials):
            material = obj.data.materials[material_index]
            if material and material.diffuse_color:
                material_color = material.diffuse_color[:3]  # Get RGB, ignore alpha

        # Iterate through the vertices of the face
        for vert in face.verts:
            # Create a tuple of the vertex position
            vert_pos = (round(vert.co.x, 4), round(vert.co.y, 4), round(vert.co.z, 4))
            vert_normal = (round(face_normal.x, 2), round(face_normal.y, 2), round(face_normal.z, 2))

            # Create a unique key for the (position, normal) combination
            unique_key = (vert_pos, vert_normal)
           
            if unique_key not in unqi_bits:
                unqi_bits.append(unique_key)
                
                unique_vertex_list.append({
                    'position': vert_pos,
                    'normal': vert_normal,
                    'color': material_color  
                })
                
                # Map the vertex position to its index
                index_mapping[unique_key] = len(unique_vertex_list) - 1

            # Add the index of the unique vertex to the index buffer
            index_buffer.append(index_mapping[unique_key])
            
         # Create edge index buffer
        for edge in face.edges:
            edge_pair = []
            for vert in edge.verts:
                vert_pos = (round(vert.co.x, 4), round(vert.co.y, 4), round(vert.co.z, 4))
                vert_normal = (round(face_normal.x, 2), round(face_normal.y, 2), round(face_normal.z, 2))

                unique_key = (vert_pos, vert_normal)
                
                index = index_mapping[unique_key]
                
                edge_pair.append(index)
                
            edge_pair = tuple(edge_pair)
                
            if edge_pair not in edge_index_buffer:
                edge_index_buffer.append(edge_pair)
                unique_edges.add(unique_key)

    # Clean up
    bm.free()
        
    return unique_vertex_list, index_buffer, edge_index_buffer

# Function to write the unique vertices and index buffer to a file
def write_to_file1(file_path, unique_vertices, index_buffer, edge_index_buffer):
    with open(file_path, 'w') as f:
        f.write("Unique Vertices with Normals:\n")
        f.write(f"vertecies: {len(unique_vertices)},\n")
        for vertex in unique_vertices:
            position_str = f"{round(vertex['position'][0] * scale_value,1)}, {round(vertex['position'][1] * scale_value,1)}, {round(vertex['position'][2] * scale_value,1)}"
            normal_str = f"{vertex['normal'][0]}, {vertex['normal'][1]}, {vertex['normal'][2]}"
            color_str = f"{round(vertex['color'][0],4)}, {round(vertex['color'][1],4)}, {round(vertex['color'][2],4)}"
            f.write(f"{position_str}, {normal_str}, {color_str}, 1.0f,\n")
           
            
            # Function to write the unique vertices and index buffer to a file
def write_to_file2(file_path, unique_vertices, index_buffer, edge_index_buffer):
    with open(file_path, 'w') as f:
        f.write("\nIndex Buffer Size and indexes:\n")
        f.write(f"{len(index_buffer)},\n")
        for i in range(0, len(index_buffer), 10):
            # Get the next 10 items (or fewer if at the end of the list)
            chunk = index_buffer[i:i + 10]
            # Write the items to the file, joined by ", "
            f.write(", ".join(map(str, chunk)) + ",\n")
            
            # Function to write the unique vertices and index buffer to a file
def write_to_file3(file_path, unique_vertices, index_buffer, edge_index_buffer):
    with open(file_path, 'w') as f:
        f.write("Unique Vertices with Normals:\n")
            
        f.write("\n LINE Index Buffer Size and indexes:\n")
        f.write(f"{len(edge_index_buffer)},\n")
        for i in range(0, len(edge_index_buffer), 10):
            # Get the next 10 items (or fewer if at the end of the list)
            chunk = edge_index_buffer[i:i + 10]
            # Format each pair as "x, y" and join them with ", "
            formatted_chunk = ", ".join(f"{x}, {y}" for x, y in chunk)
            # Write the formatted string to the file
            f.write(formatted_chunk + ", \n")  # Add a newline at the end
            
            

# Get the active object
active_obj = bpy.context.active_object

# Call the function and get the unique vertices with normals and the IBO
unique_vertices_with_normals_colors, index_buffer, edge_index_buffer = get_unique_vertices_with_normals_and_ibo(active_obj)

object_name = ("Castle2")

 
# Specify the file path where you want to save the data
file_path = ("C://Dev//BlenderExportTest")  # Save in the current Blender project directory

file_path1 = f"{file_path}//{object_name}//Verteces_VBO.txt"
file_path2 = f"{file_path}//{object_name}//Triangle_IBO.txt"
file_path3 = f"{file_path}//{object_name}//Line_IBO.txt"

# Write the results to the file
write_to_file1(file_path1, unique_vertices_with_normals_colors, index_buffer, edge_index_buffer)
write_to_file2(file_path2, unique_vertices_with_normals_colors, index_buffer, edge_index_buffer)
write_to_file3(file_path3, unique_vertices_with_normals_colors, index_buffer, edge_index_buffer)

# Print the file path for reference
print(f"Data written to: {file_path}") 



