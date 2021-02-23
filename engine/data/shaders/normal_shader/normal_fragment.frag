#version 330

out vec4 frag_color;
uniform  float time;
uniform  vec4 mesh_color;

in vec2 tex_coord;
in vec3 vertex_position;
in vec3 vertex_normal;

in vec4 vertex_blend_weight;

uniform sampler2D diffuse_texture;

void main()
{
    frag_color = mesh_color * texture(diffuse_texture, tex_coord);
}
