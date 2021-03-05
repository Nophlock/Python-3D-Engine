#version 330

out vec4 frag_color;
uniform  float time;
uniform  vec4 mesh_color;

in vec2 tex_coord;
in vec3 vertex_position;
in vec3 vertex_normal;

in vec4 vertex_blend_weight;

uniform sampler2D diffuse_texture;
uniform int has_texture;

void main()
{
    vec4 color = texture(diffuse_texture, tex_coord);
    float angle = dot(vec3(0.0, 1.0, 0.0), vertex_normal);

    if (has_texture == 0)
    {
        color = vec4(1.0);
    }

    frag_color = mesh_color * color;
}
