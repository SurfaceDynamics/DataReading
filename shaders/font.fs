#version 330 core
out vec4 FragColor;

in vec2 TexCoords;

uniform sampler2D bitMap;
uniform vec3 color;
uniform bool markString;

const float lowLim = 0.15;
const float midLim = 0.25;
const float upLim = 0.8;
const vec3 edgeColor = vec3(0.0);
const vec3 markColor = vec3(1.0);




void main()
{
    float alpha = texture(bitMap, TexCoords).a;
    if (markString == true)
        if (alpha > lowLim)
        {
            float fadeConst = smoothstep(lowLim, upLim, alpha);
            FragColor = vec4(markColor*(1 - fadeConst), 1.0);
        }
        else
            FragColor = vec4(markColor, 1.0);
    else
    {
        if (alpha <= lowLim)
            discard;
        else if (alpha <= midLim)
        {
            float fadeConst = smoothstep(lowLim, midLim, alpha);
            FragColor = vec4(edgeColor, fadeConst);
        }
        else if (alpha <= upLim)
        {
            float blendConst = smoothstep(midLim, upLim, alpha);
            FragColor = vec4(mix(edgeColor, color, blendConst), 1.0);
        }
        else
            FragColor = vec4(color, 1.0);


    }
}