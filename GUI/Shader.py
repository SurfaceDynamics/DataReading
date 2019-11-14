from OpenGL.GL import *
import ShaderLoader

class shader:
    def __init__(self, VS, FS):
        self.Shader = ShaderLoader.compile_shader(str(VS), str(FS))
    def use(self):
        glUseProgram(self.Shader)
    def bool(self, Name, Value):
        glUniform1i(glGetUniformLocation(self.Shader, str(Name)), bool(Value))
    def int(self, Name, Value):
        glUniform1i(glGetUniformLocation(self.Shader, str(Name)), int(Value))
    def float(self, Name, Value):
        glUniform1f(glGetUniformLocation(self.Shader, str(Name)), Value)
    def vec2(self, Name, Vec):
        glUniform2fv(glGetUniformLocation(self.Shader, str(Name)), 1, Vec)
    def vec3(self, Name, Vec):
        glUniform3fv(glGetUniformLocation(self.Shader, str(Name)), 1, Vec)
    def vec4(self, Name, Vec):
        glUniform4fv(glGetUniformLocation(self.Shader, str(Name)), 1, Vec)
    def mat3(self, Name, Mat):
        glUniformMatrix3fv(glGetUniformLocation(self.Shader, str(Name)), 1, GL_FALSE, Mat)
    def mat4(self, Name, Mat):
        glUniformMatrix4fv(glGetUniformLocation(self.Shader, str(Name)), 1, GL_FALSE, Mat)

