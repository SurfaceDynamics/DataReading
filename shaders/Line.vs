#version 140
in vec2 pos;

uniform mat4 model;
uniform float length;
uniform vec2 position;
void main(void)
{
    vec2 Position = pos;
    Position *= length;
    Position.x -= 1.0 - position.x*2.0;
    Position.y += 1.0 - position.y*2.0;


	gl_Position = vec4(Position, 0.0, 1.0);
}