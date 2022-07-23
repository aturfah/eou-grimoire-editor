import eel
from save_file_manager import SaveFileManager
import ui_helpers as uih

@eel.expose
def get_random_number():
    eel.prompt_alerts(7)

@eel.expose
def get_date():
    eel.prompt_alerts("doot")

@eel.expose
def load_file():
    try:
        SFM.load_file()
        if SFM.filename:
            eel.prompt_alerts("Successfully loaded file: {}".format(SFM.filename))
            return True
        else:
            return False
    except Exception as exc:
        print(exc)
        eel.prompt_alerts(str(exc))
        return False


@eel.expose
def save_file():
    try:
        output_file = SFM.save_file()
        eel.prompt_alerts("Successfully saved file: {}".format(output_file))
    except Exception as exc:
        print(exc)
        eel.prompt_alerts(str(exc))


@eel.expose
def get_grimoire_dropdown_options():
    return SFM.get_grimoire_labels()


@eel.expose
def get_skill_names():
    skill_names = list(uih.name_id_map().keys())
    skill_names.sort()

    return skill_names


@eel.expose
def get_chosen_grimoire():
    return SFM.get_chosen_grimoire()


@eel.expose
def get_chosen_grimoire_idx():
    return SFM.chosen_idx


@eel.expose
def get_grimoire_class_options():
    return list(uih.class_id_map().keys())

@eel.expose
def get_grimoire_quality_options():
    return list(uih.quality_id_map().keys())


@eel.expose
def update_chosen_grimoire(new_idx):
    if not isinstance(new_idx, int):
        new_idx = int(new_idx)

    SFM.chosen_idx = new_idx


@eel.expose
def update_grimoire_skill(idx, skill_name):
    SFM.set_grimoire_skill_name(idx, skill_name)


@eel.expose
def update_grimoire_skill_level(idx, new_level):
    SFM.set_grimoire_skill_level(idx, new_level)


@eel.expose
def update_grimoire_class(new_class):
    SFM.set_grimoire_class(new_class)


@eel.expose
def update_grimoire_quality(new_quality):
    SFM.set_grimoire_quality(new_quality)


@eel.expose
def update_grimoire_generator(new_name):
    try:
        SFM.set_grimoire_generator(new_name)
    except Exception as exc:
        eel.prompt_alerts(str(exc))

@eel.expose
def update_grimoire_unknown_origin(new_value):
    SFM.set_grimoire_unkown_origin(new_value)

@eel.expose
def update_grimoire_active(new_value):
    SFM.set_grimoire_active(new_value);


@eel.expose
def reset_grimoire():
    SFM.reset_chosen_grimoire()


if __name__ == "__main__":
    SFM = SaveFileManager()

    eel.init('web')
    eel.start('index.html', mode='default', size=(800, 600))