from hatchling.builders.hooks.plugin.interface import BuildHookInterface

class DictionaryBuildHook(BuildHookInterface):
    """ Build the dictionary """
    PLUGIN_NAME = 'dictionary'

    def initialize(self, version, build_data):
        from os import path
        from src.decapitaliza import decapitaliza

        # Spanish name particles and prepositions in lower case.
        particles = ['de', 'del', 'la', 'el', 'las', 'y', 'i', 
                    'Mc', 'Van', 'Von', 'Mac', 'Di', 'Della', 'Delle', 'Delli', 'Dello', 'Dell', 'Dels']

        compress = True
        outputfile = path.join(self.root, "src", "decapitaliza", "resources", "dictionary.bin")
        srcdir = path.join(self.root, 'src', 'dictsrc')
        
        dict = {}
        # Add prepositions to the dictionary with the key in upper case.
        for prep in particles:
            dict[prep.upper()] = prep
        # Saves the non accented words in the corpus of names and surnames to prevent subsequent accents in the dictionary from overwriting it.   
        decapitaliza.ingest_words(path.join(srcdir, "nombres.csv"), dict=dict, capitation=True, notildado=True)
        decapitaliza.ingest_words(path.join(srcdir, "apellidos.csv"), dict=dict, capitation=True, notildado=True)
        decapitaliza.ingest_words(path.join(srcdir, "rae_total.csv"), dict=dict, capitation=True, notildado=False)

        decapitaliza.write_dict_to_file(outputfile, dict, compress)

        print("Dictionary size:{0} \nWritten to: {1}".format(len(dict), outputfile))