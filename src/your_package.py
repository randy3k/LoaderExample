from foo import hello

import sublime
import sublime_plugin


class SayHello(sublime_plugin.TextCommand):
    def run(self, edit):
        sublime.message_dialog(hello())
