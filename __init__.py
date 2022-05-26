from aqt import mw
from aqt.utils import showInfo
from anki.hooks import addHook
import anki
import os
import shutil
from .Template import EDITOR, FRONT, BACK, CSS

TEMPLATENAME = "Anki X Markdown X MindMap"

FIELDS = ["Question", "Mindmap", "Answer", "Detail", "Code"]


def customizeEditor(editor):
    if editor.note.model()["name"] == TEMPLATENAME:
        editor.web.eval(EDITOR)


addHook("loadNote", customizeEditor)


def createOrUpdateTemplate():
    model = mw.col.models.byName(TEMPLATENAME)
    if not model:
        createTemplate()
    updateTemplate()


def createTemplate():
    m = mw.col.models
    model = m.new(TEMPLATENAME)

    for field in FIELDS:
        m.addField(model, m.newField(field))

    template = m.newTemplate(TEMPLATENAME)
    template["qfmt"] = FRONT
    template["afmt"] = BACK
    model["css"] = CSS

    m.addTemplate(model, template)
    m.add(model)
    m.save(model)


def updateTemplate():
    model = mw.col.models.byName(TEMPLATENAME)
    model["tmpls"][0]["qfmt"] = FRONT
    model["tmpls"][0]["afmt"] = BACK
    model["css"] = CSS

    mw.col.models.save(model)

    addonFolder = os.path.join(os.path.dirname(os.path.realpath(__file__)))
    assetsFolder = os.path.join(addonFolder, "assets")
    mediaFolder = mw.col.media.dir()
    for assetName in os.listdir(assetsFolder):
        assetFullPath = os.path.join(assetsFolder, assetName)
        if not os.path.exists(os.path.join(mediaFolder, assetName)):
            mw.col.media.add_file(assetFullPath)


addHook("profileLoaded", createOrUpdateTemplate)
