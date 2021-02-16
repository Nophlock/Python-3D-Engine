

#version 330
layout (location = 0) in vec3 position;
layout (location = 1) in vec2 uv;
layout (location = 2) in vec3 normal;
layout (location = 3) in vec4 tangent;
layout (location = 4) in vec4 blend_index;
layout (location = 5) in vec4 blend_weight;

uniform mat4 transformation_matrix;
uniform mat4 camera_matrix;
uniform mat4 perspective_matrix;

uniform mat3x4 bone_matrices[100];

out vec3 vertex_position;
out vec3 vertex_normal;
out vec2 tex_coord;
out vec4 vertex_blend_weight;

void main()
{
	vertex_position = position;
	vertex_normal	= normal;
	tex_coord = vec2(uv.x, 1.0 - uv.y);

	vertex_blend_weight = blend_weight;

	mat3x4 bone_matrix = bone_matrices[int(blend_index.x)] * blend_weight.x;
	bone_matrix += bone_matrices[int(blend_index.y)] * blend_weight.y;
	bone_matrix += bone_matrices[int(blend_index.z)] * blend_weight.z;
	bone_matrix += bone_matrices[int(blend_index.w)] * blend_weight.w;

	vec4 skeletal_vec = vec4( vec4(position, 1.0) * bone_matrix, 1.0);

	vec4 t_vector = perspective_matrix * camera_matrix * transformation_matrix * skeletal_vec;
	gl_Position 	= t_vector;
}
