#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec2 aTexCoords;
layout (location = 2) in vec2 texStart;
layout (location = 3) in vec2 texScale;
layout (location = 4) in vec2 posList;
layout (location = 5) in vec2 scaleList;


out vec2 TexCoords;

uniform vec2 position;
uniform vec2 centerPos;
uniform vec2 screenSize;
void main()
{
    TexCoords = vec2(texStart.x + texScale.x * aTexCoords.x,
                     texStart.y + texScale.y * aTexCoords.y);
    vec3 Position = aPos;
    Position.x *= scaleList.x/screenSize.x;
    Position.y *= scaleList.y/screenSize.y;
    Position.x += posList.x/screenSize.x + centerPos.x + position.x/screenSize.x;
    Position.y += posList.y/screenSize.y + centerPos.y + position.y/screenSize.y;


    gl_Position = vec4(Position, 1.0);
}