eel.expose(prompt_alerts);
function prompt_alerts(description) {
  alert(description);
}

// Set the elements in the grimoire dropdown list
async function setGrimoireDropdown() {
  let grimoireList = await eel.get_grimoire_dropdown_options()()

  const grimoireDropdown = document.getElementById("grimoire-dropdown");

  // In case we're re-calling this, delete
  while(grimoireDropdown.firstChild) {
    grimoireDropdown.removeChild(grimoireDropdown.firstChild)
  }

  // Fill the children
  grimoireList.forEach((name, idx) => {
    let opt = document.createElement("option");
    opt.value = idx;
    opt.innerHTML = name;
    grimoireDropdown.appendChild(opt);
  });

  // Set the value correctly
  grimoireDropdown.value = await eel.get_chosen_grimoire_idx()();
}

// Set the elements in the grimoire class dropdown
async function setGrimoireClassDropdown() {
  let grimClasses = await eel.get_grimoire_class_options()()

  const classDropdown = document.getElementById("grim-class")

  grimClasses.forEach(name => {
    let opt = document.createElement("option")
    opt.value = name
    opt.innerHTML = name
    classDropdown.appendChild(opt)
  })
}

// Set the elements in the skill selection dropdown
async function setSkillNameDropdown() {
  let skillList = await eel.get_skill_names()()

  skillList.forEach(val => {
    for (let idx=0; idx < 7; idx++) {
      const opt = document.createElement("option");
      opt.value = val;
      opt.innerHTML = val;  
      document.getElementById("skill-name"+idx).appendChild(opt);
    }
  });
}

// Set the elements in the grimoire quality dropdown
async function setGrimoireQualityDropdown() {
  let qualityList = await eel.get_grimoire_quality_options()();

  const qualityDropdown = document.getElementById("grim-quality");

  qualityList.forEach(name => {
    let opt = document.createElement("option")
    opt.value = name
    opt.innerHTML = name
    qualityDropdown.appendChild(opt)
  })
}

function updateGrimoireGeneratorReadOnly(grimOriginUnk) {
  const grimGeneratorField = document.getElementById("grim-generator");
  grimGeneratorField.readOnly = grimOriginUnk;
  if (grimOriginUnk === true) {
    grimGeneratorField.classList.add("greyed-out")
  } else {
    grimGeneratorField.classList.remove("greyed-out")
  }
}

// Render the chosen Grimoire
async function renderChosenGrimoire() {
  const grimoireDatum = await eel.get_chosen_grimoire()()

  const grimoireClass = document.getElementById("grim-class");
  grimoireClass.value = grimoireDatum.class;

  const grimoireQuality = document.getElementById("grim-quality");
  grimoireQuality.value = grimoireDatum.quality;

  const grimOriginUnk = document.getElementById("grim-unk-origin");
  grimOriginUnk.checked = grimoireDatum.unknown_origin;
  updateGrimoireGeneratorReadOnly(grimoireDatum.unknown_origin);

  const grimGenerator = document.getElementById("grim-generator");
  grimGenerator.value = grimoireDatum["name"];

  grimoireDatum["skills"].forEach((val, idx) => {
    // Set the skill name
    let skillNameSelect = document.getElementById("skill-name"+idx);
    skillNameSelect.value = val["name"];

    // Set the grimire level
    let skillLevelSelect = document.getElementById("skill-level"+idx)
    skillLevelSelect.value = String(val["level"]);
  })
}

// When the grimoire dropdown is changed, update the python class
async function grimoireSelectCallback() {
  const newIdx = document.getElementById("grimoire-dropdown").value;
  await eel.update_chosen_grimoire(newIdx)();
  
  // Update the panel
  renderChosenGrimoire();
}


// When the skill select dropdown is changed, update the python class
async function skillSelectCallback(idx) {
  const newSkill = document.getElementById("skill-name"+idx).value;
  await eel.update_grimoire_skill(idx, newSkill)();

  // Update the panel
  setGrimoireDropdown();
  renderChosenGrimoire();
}

// When the skill level is changed, update the python class
async function skillLevelCallback(idx) {
  const newLevel = document.getElementById("skill-level"+idx).value;
  await eel.update_grimoire_skill_level(idx, newLevel);

  // Update the panel
  setGrimoireDropdown();
  renderChosenGrimoire();
}

// When the grimoire class is changed, update the python class
async function grimoreClassCallback() {
  const newClass = document.getElementById("grim-class").value;
  await eel.update_grimoire_class(newClass);

  // Update the panel
  setGrimoireDropdown();
  renderChosenGrimoire();
}

// When the grimoire quality is changed, update the python class
async function grimoreQualityCallback() {
  const newQual = document.getElementById("grim-quality").value;
  await eel.update_grimoire_quality(newQual);

  // Update the panel
  setGrimoireDropdown();
  renderChosenGrimoire();
}

async function grimoireGeneratorCallback() {
  const newGenerator = document.getElementById("grim-generator").value;
  await eel.update_grimoire_generator(newGenerator);

  setGrimoireDropdown();
  renderChosenGrimoire();
}

async function grimoireUnknownOriginCallback() {
  const grimOriginUnk = document.getElementById("grim-unk-origin").checked;

  // Set the grimoire generator to unable to be edited if Unknown
  updateGrimoireGeneratorReadOnly(grimOriginUnk)

  await eel.update_grimoire_unknown_origin(grimOriginUnk);

  setGrimoireDropdown();
  renderChosenGrimoire();
}

// Load the file from disk and prepare UI
async function loadMethod() {
  const success = await eel.load_file()();

  if (success === false) {
    return;
  }

  // Get everything prepared
  setGrimoireDropdown();
  setSkillNameDropdown();
  setGrimoireClassDropdown();
  setGrimoireQualityDropdown();
  renderChosenGrimoire();

  // Reset/Save buttons are allowed
  document.getElementById("reset-button").removeAttribute("disabled")
  document.getElementById("save-button").removeAttribute("disabled")

  // Add functionality after load
  document.getElementById("save-button").addEventListener("click", ()=>{saveMethod()}, false);
  document.getElementById("reset-button").addEventListener("click", ()=>{resetMethod()}, false);
}

// Reset grimoire to original stats
async function resetMethod() {
  await eel.reset_grimoire()();

  // Update the panel
  setGrimoireDropdown();
  renderChosenGrimoire();
}

// Save file
async function saveMethod() {
  await eel.save_file()();

  // Update the panel
  setGrimoireDropdown();
  renderChosenGrimoire();
}


// Assign functionality to buttons
document.getElementById("load-button").addEventListener("click", ()=>{loadMethod()}, false);