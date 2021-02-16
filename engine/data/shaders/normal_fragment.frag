#version 330

out vec4 frag_color;
uniform  float time;

in vec2 tex_coord;
in vec3 vertex_position;
in vec3 vertex_normal;

in vec4 vertex_blend_weight;

uniform sampler2D diffuse_texture;

void main()
{
	//float value = dot(vertex_normal, vec3(0.0, 1.0, 0.0) );

	//frag_color = vertex_blend_weight;

    frag_color = texture(diffuse_texture, tex_coord);
}
