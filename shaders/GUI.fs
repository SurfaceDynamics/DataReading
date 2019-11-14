#version 140

in vec2 textureCoords;

out vec4 out_Color;

uniform sampler2D texture1;

uniform int type;
uniform vec3 mainColor;
uniform vec3 edgeColor;

uniform float edge;
uniform float baseAlpha;
uniform float aspectRatio;
uniform float slidebarPercent;
uniform bool edgeFlip;
uniform bool rowMarker;
uniform int numberOfMatrixRows;
uniform int numberOfMatrixCol;
uniform int currentMatrixRow;

void main(void)
{
	if (type == 0)
		out_Color = texture(texture1, textureCoords);
	else
	{
		vec2 coords = vec2(textureCoords.x, textureCoords.y);
		if (edgeFlip == true)
		{
			coords = vec2(1.0 - coords.y, coords.x);
		}
		if ((coords.x > edge*aspectRatio) && (coords.x <= (1.0 - edge*aspectRatio)) && (coords.y > edge) && (coords.y <= (1.0 - edge)))
		{
			if (type == 1)
				out_Color = vec4(mainColor, baseAlpha);
			else if (type == 2)
			{
				if ((coords.x - edge*2.0*aspectRatio)/(1.0 - edge*2.0*aspectRatio) + edge*aspectRatio < slidebarPercent)
					out_Color = vec4(mix(mainColor, edgeColor, 0.5), baseAlpha);
				else
					out_Color = vec4(mainColor, baseAlpha);
			}
			else if (type == 3)
			{
			    float currentRow = floor(coords.y*numberOfMatrixRows);
                if (currentRow == currentMatrixRow)
                    if (rowMarker == true)
                        out_Color = vec4(mainColor, baseAlpha);
                    else
                        out_Color = vec4(mainColor*0.35, baseAlpha);
                else
                {
                    float currentCol = floor(coords.x*numberOfMatrixCol);
                    if (mod(currentCol, 2.0) == 0)
                        out_Color = vec4(vec3(0.0), baseAlpha);
                    else
                        out_Color = vec4(mainColor*0.15, baseAlpha);
                }

			}
		}
		else
		{
			out_Color = vec4(edgeColor, baseAlpha);
		}


	}

}