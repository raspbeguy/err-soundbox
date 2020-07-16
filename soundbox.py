from errbot import BotPlugin, botcmd
import subprocess

class Sound():
    def __init__(self, filename, aliases):
        self.filename = filename
        self.aliases = aliases
        self.counter = 0

    def play(self, sounds_path):
        proc = subprocess.Popen(['mpv', '--really-quiet', sounds_path+"/"+self.filename])
        self.counter += 1
        return proc

    def addAliases(self, aliases):
        self.aliases = list(set(self.aliases + aliases))

    def getAliases(self):
        return self.aliases

    def getFilename(self):
        return self.filename

    def __str__(self):
        return "{}\t{}".format(self.filename, ", ".join(self.aliases))

    def __eq__(self, other):
        if not isinstance(other, Sound):
            return False
        return self.filename == other.getFilename

class Soundbox(BotPlugin):
    """Plugin to play funny sounds"""

    def activate(self):
        super().activate()
        self.mute = False
        self.proc = None
        if "SOUNDS" not in self:
            self["SOUNDS"]=[]

    def get_configuration_template(self):
        return {'SOUNDS_PATH': '/srv/sounds'}

    @botcmd
    def soundbox_list(self, msg, args):
        """List sounds"""
        for sound in self['SOUNDS']:
            yield str(sound)
        if len(self['SOUNDS']) == 0:
            return "No sounds yet"

    @botcmd(split_args_with=None)
    def soundbox_add(self, msg, args):
        """Add a sound"""
        sound = Sound(args[0],args[1:])
        with self.mutable('SOUNDS') as sounds_list:
            sounds_list.append(sound)
        return "Sound was successfully added."

    def findSound(self, alias):
        for sound in self['SOUNDS']:
            if alias in sound.aliases:
                return sound
        return None

    @botcmd(split_args_with=None)
    def soundbox_addaliases(self, msg, args):
        """Add a list of aliases to a sound"""
        sound = self.findSound(args[0])
        if sound == None:
            return "Sound {} not found.".format(args[0])
        sound.addAliases(args[:1])
        return "Aliases were successfully added."

    @botcmd
    def soundbox_del(self, msg, args):
        """Remove a sound"""
        sound = self.findSound(args)
        if sound == None:
            return "Sound {} not found.".format(args)
        with self.mutable('SOUNDS') as sounds_list:
            sounds_list.remove(sound)
        return "Sound was successfully removed."

    @botcmd
    def sb(self, msg, args):
        """Play a sound"""
        if self.mute:
            return "Mmmh mmh mmmmh! (My lips are sealed!)"
        elif self.proc and self.proc.poll() is None:
            return "I'm already playing something!"
        else:
            sound = self.findSound(args)
            if sound == None:
                return "Sound {} not found.".format(args)
            self.proc = sound.play(self.config["SOUNDS_PATH"])

    @botcmd
    def kill(self, msg, args):
        """Kill current sound"""
        self.proc.terminate()
        return "OK, sorry if it was too loud..."

    @botcmd
    def mute(self, msg, args):
        """Disables temporarly making noise"""
        if self.mute:
            self.mute=False
            return "Yay, I can make noise again!"
        else:
            self.mute=True
            return "OK, I'll shut up now!"
