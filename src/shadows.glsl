#define N 300

// x, y position of the light
uniform vec2 lightPosition;
// Size of light in pixels
uniform float lightSize;

float terrain(vec2 samplePoint)
{
    float samplePointAlpha = texture(iChannel0, samplePoint).a;
    float sampleStepped = step(0.1, samplePointAlpha);
    float returnValue = 1.0 - sampleStepped;

    // Soften the shadows. Comment out for hard shadows.
    // The closer the first number is to 1.0, the softer the shadows.
    returnValue = mix(0.9, 1.0, returnValue);

    return returnValue;
}

void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
    // Normalize the fragment coordinate from (0.0, 0.0) to (1.0, 1.0)
    vec2 fragCoord2 = fragCoord + 0; 
    vec2 lightPosition2 = lightPosition * 1.25;
    vec2 iResolution2 = iResolution.xy * 1.25;
    vec2 normalizedFragCoord = fragCoord2/iResolution2.xy;
    vec2 normalizedLightCoord = lightPosition2.xy/iResolution2.xy;

    // Distance in pixels to the light
    float distanceToLight = length(lightPosition2 - fragCoord2);


    // Start our mixing variable at 1.0
    float lightAmount = 1.0;
    for(float i = 0.0; i < N; i++)
    {
        // A 0.0 - 1.0 ratio between where our current pixel is, and where the light is
        float t = i / N;
        // Grab a coordinate between where we are and the light
        vec2 samplePoint = mix(normalizedFragCoord, normalizedLightCoord, t);
        // Is there something there? If so, we'll assume we are in shadow
	    float shadowAmount = terrain(samplePoint);
        // Multiply the light amount.
        // (Multiply in case we want to upgrade to soft shadows)
        lightAmount *= shadowAmount;
    }

    // Find out how much light we have based on the distance to our light
    lightAmount *= 1.0 - smoothstep(0.0, lightSize, distanceToLight);

    // We'll alternate our display between black and whatever is in channel 1
    vec4 blackColor = vec4(0.0, 0.0, 0.0, 1.0);

    // Our fragment color will be somewhere between black and channel 1
    // dependent on the value of b.
    fragColor = mix(blackColor, texture(iChannel1, normalizedFragCoord), lightAmount);
}