import bpy

class LightSetup:
    def __init__(self):
        self.lights = []

    def make(self, name, texture):
        return self._make(name, texture)

    def _activate(self, name, value=False):
        bpy.data.collections[name].hide_render = value
        bpy.data.collections[name].hide_viewport = value

    def _control_rgb(self, light):
        _nodes = [x for x in light.node_tree.nodes if "RGB" in x.name]
        if len(_nodes) != 0:
            for n in _nodes:
                light.node_tree.nodes.remove(n)
        emission_node = self._control_emission(light)
        
        
        return emission_node

    def _control_emission(self, light):
        _nodes = [x for x in light.node_tree.nodes if "Emission" in x.name]
        if len(_nodes)>0:
            sockets = [x for x in _nodes[0].inputs if "Color" in x.name]
            if len(sockets)>0:
                sockets[0].enabled = True
                return _nodes[0]
        node = light.node_tree.nodes.new("ShaderNodeEmission")
        output = self._control_output(light)
        _ = light.node_tree.links.new(node.outputs[0], output.inputs[0])
        return node

    def _control_output(self, light):
        try:
            return light.node_tree.nodes["Light Output"]
        except Exception:
            return light.node_tree.nodes.new("ShaderNodeOutputLight")

    def _detach_image_node(self, light):
        if light.node_tree:
            _nodes = [x for x in light.node_tree.nodes if "Emission" in x.name]
            if _nodes:
                _node = _nodes[0]
                _node.inputs[0].enabled = False

    def _get_lights(self, name):
        light_collection = bpy.data.collections[name]    
        return [x.name for x in light_collection.all_objects if not "empty" in x.name.lower()]

    def _make(self, name, texture):
        self.lights = self._get_lights(name)
        for light in self.lights:
            try:
                l = bpy.data.objects[light].data
            except KeyError or AttributeError:
                l = bpy.data.lights[light]
            if l.use_nodes:
                try:
                    # self._update_image(l, texture.content) - to update with an image
                    self._detach_image_node(l)
                    self._update_rgb(l, texture)
                except Exception as e:
                    #try:
                    self._detach_image_node(l)
                    self._update_rgb(l, texture)
                        
                    # except Exception as e:
                    #     print(light, texture)
                    #     print(repr(e))
        self._activate(name)

    def _update_image(self, light, value):
        if light.node_tree:
            _nodes = [x for x in light.node_tree.nodes if "Image Texture" in x.name]
            for n in _nodes:
                n.image = value  # texture.content

    def _update_rgb(self, light, value):
        
        n = self._control_rgb(light)
        gamma = 2.2
        values = [pow(int(value[x:x+2], 16)/ 255., gamma) for x in range(0, 6, 2)]
        # if light.node_tree:
        #     _nodes = [x for x in light.node_tree.nodes if "RGB" in x.name]
        # for n in _nodes:
        for i in range(len(values)):
            n.inputs[0].default_value[i] = values[i]  # texture.content

        # for node in light.node_tree.nodes:
        #     node.select = False
        # n.select = True
        # light.node_tree.nodes.active = n
        # n.update()
