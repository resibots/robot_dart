#ifndef NEW_GLSL
#define in varying
#define color gl_FragColor
#define texture texture2D
#endif

#ifndef RUNTIME_CONST
#define const
#endif

#define M_PI 3.1415926535897932384626433832795

struct lightSource
{
    highp vec4 position;
    highp vec4 ambient;
    highp vec4 diffuse;
    highp vec4 specular;
    highp vec3 spotDirection;
    highp float spotExponent;
    highp float spotCutoff;
    highp float intensity;
    highp float constantAttenuation;
    highp float linearAttenuation;
    highp float quadraticAttenuation;
    highp vec4 worldPosition;
};

#ifdef EXPLICIT_UNIFORM_LOCATION
layout(location = 3)
#endif
uniform mediump float shininess
    #ifndef GL_ES
    = 80.0
    #endif
    ;

#ifdef AMBIENT_TEXTURE
#ifdef EXPLICIT_TEXTURE_LAYER
layout(binding = 0)
#endif
uniform lowp sampler2D ambientTexture;
#endif

#ifdef EXPLICIT_UNIFORM_LOCATION
layout(location = 4)
#endif
uniform lowp vec4 ambientColor
    #ifndef GL_ES
    #ifndef AMBIENT_TEXTURE
    = vec4(0.0, 0.0, 0.0, 1.0)
    #else
    = vec4(1.0)
    #endif
    #endif
    ;

#ifdef DIFFUSE_TEXTURE
#ifdef EXPLICIT_TEXTURE_LAYER
layout(binding = 1)
#endif
uniform lowp sampler2D diffuseTexture;
#endif

#ifdef EXPLICIT_UNIFORM_LOCATION
layout(location = 5)
#endif
uniform lowp vec4 diffuseColor
    #if !defined(GL_ES) && defined(DIFFUSE_TEXTURE)
    = vec4(1.0)
    #endif
    ;

#ifdef SPECULAR_TEXTURE
#ifdef EXPLICIT_TEXTURE_LAYER
layout(binding = 2)
#endif
uniform lowp sampler2D specularTexture;
#endif

#ifdef EXPLICIT_UNIFORM_LOCATION
layout(location = 6)
#endif
uniform lowp vec4 specularColor
    #ifndef GL_ES
    = vec4(1.0)
    #endif
    ;

#ifdef EXPLICIT_TEXTURE_LAYER
layout(binding = 3)
#endif
uniform sampler2DArrayShadow shadowTextures;

#ifdef EXPLICIT_TEXTURE_LAYER
layout(binding = 4)
#endif
uniform samplerCubeArrayShadow cubeMapTextures;

#ifdef EXPLICIT_UNIFORM_LOCATION
layout(location = 8)
#endif
uniform float farPlane;

#ifdef EXPLICIT_UNIFORM_LOCATION
layout(location = 9)
#endif
uniform bool isShadowed;

#ifdef EXPLICIT_UNIFORM_LOCATION
layout(location = 10)
#endif
uniform lightSource lights[LIGHT_COUNT];

in mediump vec3 transformedNormal;
in highp vec3 cameraDirection;
in highp vec3 worldPosition;
in highp vec4 lightSpacePositions[LIGHT_COUNT];

#if defined(AMBIENT_TEXTURE) || defined(DIFFUSE_TEXTURE) || defined(SPECULAR_TEXTURE)
in mediump vec2 interpolatedTextureCoords;
#endif

#ifdef NEW_GLSL
out lowp vec4 color;
#endif

float visibilityCalculation(int index, float bias)
{
    vec4 fragPosLightSpace = lightSpacePositions[index];
    // perform perspective divide
    vec3 projCoords = fragPosLightSpace.xyz / fragPosLightSpace.w;
    // transform to [0,1] range
    // projCoords = projCoords * 0.5 + 0.5;
    // get depth of current fragment from light's perspective
    float currentDepth = projCoords.z;
    if(currentDepth > 1.)// || projCoords.x < 0. || projCoords.x >= 1. || projCoords.y < 0. || projCoords.y >= 1.)
        return 1.;
    // float visibility = texture(shadowTextures, vec4(projCoords.xy, index, currentDepth - bias));
    float visibility = 0.;
    vec2 texelSize = 0.5 / textureSize(shadowTextures, 0).xy;
    for(int x = -1; x <= 1; ++x)
        for(int y = -1; y <= 1; ++y)
            visibility += texture(shadowTextures, vec4(projCoords.xy + vec2(x, y) * texelSize, index, currentDepth - bias));
    visibility /= 9.;

    return 1. - 0.7*(1. - visibility);
}

float visibilityCalculationPointLight(int index, float bias)
{
    vec3 sampleOffsetDirections[20] = vec3[]
    (
        vec3( 1,  1,  1), vec3( 1, -1,  1), vec3(-1, -1,  1), vec3(-1,  1,  1),
        vec3( 1,  1, -1), vec3( 1, -1, -1), vec3(-1, -1, -1), vec3(-1,  1, -1),
        vec3( 1,  1,  0), vec3( 1, -1,  0), vec3(-1, -1,  0), vec3(-1,  1,  0),
        vec3( 1,  0,  1), vec3(-1,  0,  1), vec3( 1,  0, -1), vec3(-1,  0, -1),
        vec3( 0,  1,  1), vec3( 0, -1,  1), vec3( 0, -1, -1), vec3( 0,  1, -1)
    );

    vec3 direction = worldPosition - lights[index].worldPosition.xyz;
    float depth = length(direction)/farPlane;
    if(depth > 1.)
        return 1.;
    float visibility = 0.;
    float diskRadius = 0.002;//(1.0 + (length(cameraDirection) / farPlane)) / 50.0;//0.01;
    for(int i = 0; i < 20; ++i)
        visibility += texture(cubeMapTextures, vec4(normalize(direction) + sampleOffsetDirections[i] * diskRadius, index), depth - bias);
    visibility /= 20.;

    return 1. - 0.7*(1. - visibility);
}

void main() {
    lowp const vec4 finalAmbientColor =
        #ifdef AMBIENT_TEXTURE
        texture(ambientTexture, interpolatedTextureCoords)*
        #endif
        ambientColor;
    lowp const vec4 finalDiffuseColor =
        #ifdef DIFFUSE_TEXTURE
        texture(diffuseTexture, interpolatedTextureCoords)*
        #endif
        diffuseColor;
    lowp const vec4 finalSpecularColor =
        #ifdef SPECULAR_TEXTURE
        texture(specularTexture, interpolatedTextureCoords)*
        #endif
        specularColor;

    /* Ambient color */
    color = finalAmbientColor;

    mediump vec3 normalizedTransformedNormal = normalize(transformedNormal);

    for(int i = 0; i != LIGHT_COUNT; ++i) {
        highp vec3 lightDirection;
        highp float attenuation;
        bool spec = any(greaterThan(lights[i].specular.rgb, vec3(0.0)));
        bool isPoint = false;

         if(!any(greaterThan(lights[i].diffuse.rgb, vec3(0.0))) && !spec)
            continue;

        /* Directional light */
        if(lights[i].position.w == 0.0) {
            attenuation = lights[i].intensity;
            lightDirection = normalize(-vec3(lights[i].position));
        }
        /* Pointlight or Spotlight */
        else {
            /* cameraDirection = -transformedPosition */
            lightDirection = vec3(lights[i].position) + cameraDirection;

            highp float distance = length(lightDirection);

            attenuation = lights[i].intensity / (lights[i].constantAttenuation +
                                                    distance * (lights[i].linearAttenuation + distance * lights[i].quadraticAttenuation));

            lightDirection = normalize(lightDirection);

            /* Spotlight */
            if(lights[i].spotCutoff < M_PI/2.0) {
                float clampedCosine = max(0.0, dot(-lightDirection, lights[i].spotDirection));
                /* Outsise of spotlight cone? */
                if(clampedCosine < cos(lights[i].spotCutoff)) {
                    attenuation = 0.0;
                }
                else {
                    attenuation = attenuation * pow(clampedCosine, lights[i].spotExponent);
                }
            }
            else
                isPoint = true;
        }

        highp float intensity = dot(normalizedTransformedNormal, lightDirection);
        float visibility = 1.;
        if(isShadowed) {
            float bias = 0.00002;//max(0.0001, 0.0005*tan(acos(intensity)));//0.001;// max(0.05 * (1.0 - intensity), 0.005);
            if(!isPoint)
                visibility = visibilityCalculation(i, bias);
            else {
                bias = 0.002;
                visibility = visibilityCalculationPointLight(i, bias);
            }
        }

        /* Diffuse color */
        highp vec4 diffuseReflection = attenuation * lights[i].diffuse * finalDiffuseColor * max(0.0, intensity);

        highp vec4 specularReflection = vec4(0.0, 0.0, 0.0, 1.0);

        /* Specular color if needed */
        if(intensity > 0.0 && spec) {
            highp vec3 reflection = reflect(-lightDirection, normalizedTransformedNormal);
            highp float specularity = pow(max(0.0, dot(normalize(cameraDirection), reflection)), shininess + 1e-8);
            specularReflection = attenuation * lights[i].specular * finalSpecularColor * specularity;
        }

        color += (diffuseReflection + specularReflection) * visibility;
    }
}