# Extends Sublime Text autocompletion to find matches in all open
# files. By default, Sublime only considers words from the current file.

import sublime_plugin
import sublime
import os, sys

sys.path.append(os.path.dirname(__file__))

import commentjson


class VINSAutocomplete(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        print("VINSAutocomplete")

        cur_path = view.file_name()
        cur_intent, extension = os.path.basename(cur_path).split('.')
        if extension not in ['nlu', 'nlg']:
            return None
        cur_dir = os.path.dirname(cur_path)
        pathes = [
            cur_dir + "/VinsProjectfile.js",
            cur_dir + "/../VinsProjectfile.js",
            cur_dir + "/../../VinsProjectfile.js",
            cur_dir + "/../../../VinsProjectfile.js",        
            cur_dir + "/Vinsfile.js",
            cur_dir + "/../Vinsfile.js",
            cur_dir + "/../../Vinsfile.js",
            cur_dir + "/../../../Vinsfile.js",
        ]
        for path in pathes:
            if os.path.exists(path):
                try:
                    with open(path, "r") as f_vinsfile:
                        cfg = commentjson.load(f_vinsfile)
                        if path.endswith('Vinsfile.js'):
                            cfg = cfg['project']

                        for intent_cfg in cfg['intents']:
                            intent = intent_cfg['intent']
                            if intent_cfg.get('dm') is None:
                                continue
                            intent_path = intent_cfg['dm']['path']
                            if intent == cur_intent:
                                root_dir = os.path.dirname(path)
                                intent_full_path = "%s/%s" % (
                                    root_dir,
                                    intent_path
                                )
                                with open(intent_full_path, "r") as f_intent:
                                    intent_cfg = commentjson.load(f_intent)
                                    all_slots = [
                                        slot['slot']
                                        for slot in intent_cfg["slots"]
                                    ]

                                    matches = [
                                        ("%s\t%s" % (slot, intent), "%s" % slot)
                                        for slot in all_slots
                                        if slot
                                    ]

                                    # matches = [
                                    #     (
                                    #         "location_from1\torder_taxi",
                                    #         "location_from1"
                                    #     ),
                                    #     (
                                    #         "location_to1\torder_taxi",
                                    #         "location_to1"
                                    #     ),
                                    #     (
                                    #         "when1\torder_taxi",
                                    #         "when1"
                                    #     )
                                    # ]

                                    return (matches, sublime.INHIBIT_WORD_COMPLETIONS)

                except Exception as e:
                    print(e)
                    return None
                break

        return None
