import json

class ReadFile():
    
    def ReadFile(self, File):
        with open(File) as json_file:
            data = json.load(json_file)
        return data
        
    def GetParams(self, x):
        self.particles_radius = x.get('particles_radius')
        self.particles_count = x.get('particles_count')
        self.particles_sides_count = x.get('particles_sides_count')
        self.iters_count = x.get('iters_count')