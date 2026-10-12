const API_ROOT = window.location.origin;
const webApp = window.Telegram?.WebApp;
const ownerId = webApp?.initDataUnsafe?.user?.id;
const initData = webApp?.initData;

const state = {
  section: "todos",
  entries: [],
  language: localStorage.getItem("note-bot-language") || "ar",
  theme: localStorage.getItem("note-bot-theme") || "system",
  editing: null,
};

const translations = {
  ar: {
    languageName: "عربي",
    theme: { system: "النظام", light: "نهاري", dark: "ليلي" },
    eyebrow: "مساحتك الهادئة",
    title: "مذكّرتي",
    subtitle: "رتّب يومك واحتفظ بأفكارك وأشيائك المهمة بمكان واحد.",
    section: { notes: "ملاحظاتك", todos: "مهامك", secrets: "أسرارك" },
    add: "إضافة",
    addNew: { notes: "أضف ملاحظة", todos: "أضف مهمة", secrets: "أضف سراً" },
    nav: { notes: "ملاحظات", todos: "المهام", secrets: "أسرار" },
    emptyTitle: { notes: "ما عندك ملاحظات بعد", todos: "قائمتك فارغة", secrets: "ما عندك أسرار محفوظة" },
    emptyCopy: { notes: "أضف أول ملاحظة وخلي أفكارك قريبة.", todos: "أضف مهمة جديدة حتى تبدأ بتنظيم يومك.", secrets: "احفظ معلومة مهمة هنا حتى ترجع لها بسهولة." },
    dialogNew: { notes: "ملاحظة جديدة", todos: "مهمة جديدة", secrets: "سر جديد" },
    dialogEdit: { notes: "تعديل الملاحظة", todos: "تعديل المهمة", secrets: "تعديل السر" },
    noteLabel: "نص الملاحظة",
    todoLabel: "المهمة",
    secretTitleLabel: "العنوان",
    secretValueLabel: "المعلومة السرية",
    notePlaceholder: "اكتب ملاحظتك هنا...",
    todoPlaceholder: "شنو الشي اللي تريد تسويه؟",
    secretTitlePlaceholder: "مثال: رمز الخزنة",
    secretValuePlaceholder: "اكتب المعلومة هنا",
    save: "حفظ",
    update: "حفظ التعديل",
    cancel: "إلغاء",
    edit: "تعديل",
    delete: "حذف",
    confirmDelete: "متأكد تريد تحذف هذا العنصر؟",
    missingTelegram: "افتح الميني آب من داخل بوت تيليغرام حتى نعرض بياناتك.",
    loadError: "ما قدرنا نوصل للبيانات. تأكد أن الخدمة شغالة وحاول مرة ثانية.",
    saveError: "ما قدرنا نحفظ التغيير. حاول مرة ثانية.",
    deleteError: "ما قدرنا نحذف العنصر. حاول مرة ثانية.",
    emptyField: "اكتب قيمة قبل الحفظ.",
  },
  en: {
    languageName: "English",
    theme: { system: "System", light: "Light", dark: "Dark" },
    eyebrow: "A little space for you",
    title: "My Notes",
    subtitle: "Keep your day, thoughts, and important things together.",
    section: { notes: "Your notes", todos: "Your tasks", secrets: "Your secrets" },
    add: "Add",
    addNew: { notes: "Add a note", todos: "Add a task", secrets: "Add a secret" },
    nav: { notes: "Notes", todos: "To-do", secrets: "Secrets" },
    emptyTitle: { notes: "No notes yet", todos: "Your list is empty", secrets: "No saved secrets" },
    emptyCopy: { notes: "Add your first note to keep an idea close.", todos: "Add a task to start organizing your day.", secrets: "Save something important here for later." },
    dialogNew: { notes: "New note", todos: "New task", secrets: "New secret" },
    dialogEdit: { notes: "Edit note", todos: "Edit task", secrets: "Edit secret" },
    noteLabel: "Note",
    todoLabel: "Task",
    secretTitleLabel: "Title",
    secretValueLabel: "Secret value",
    notePlaceholder: "Write your note...",
    todoPlaceholder: "What do you need to do?",
    secretTitlePlaceholder: "For example: Safe code",
    secretValuePlaceholder: "Write the secret here",
    save: "Save",
    update: "Save changes",
    cancel: "Cancel",
    edit: "Edit",
    delete: "Delete",
    confirmDelete: "Are you sure you want to delete this item?",
    missingTelegram: "Open the Mini App from your Telegram bot to view your data.",
    loadError: "Couldn't load your data. Check that the service is running and try again.",
    saveError: "Couldn't save this change. Please try again.",
    deleteError: "Couldn't delete this item. Please try again.",
    emptyField: "Enter a value before saving.",
  },
};

const sectionMeta = {
  notes: {
    path: "/get_notes",
    addPath: "/add_notes",
    updatePath: "/update_notes",
    deletePath: "/delete_notes",
    idKey: "note_id",
    valueKey: "text",
  },
  todos: {
    path: "/get_todos",
    addPath: "/add_todos",
    updatePath: "/update_todos",
    deletePath: "/delete_todos",
    idKey: "todo_id",
    valueKey: "task",
  },
  secrets: {
    path: "/get_secrets",
    addPath: "/add_secrets",
    updatePath: "/update_secrets",
    deletePath: "/delete_secrets",
    idKey: "secret_id",
  },
};

const icons = {
  notes: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 5.5h14v13H9l-4 2v-15ZM8.5 10h7M8.5 14h5"/></svg>',
  todos: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 4.5h12v15H6zM9 8h6M9 12h3M9 16h2M15 11l3 3 3.5-4"/></svg>',
  secrets: '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="8" r="3.2"/><path d="M5.5 20a6.5 6.5 0 0 1 13 0M4 20h16"/></svg>',
  edit: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m4 16.5-.8 4.3 4.3-.8L19 8.5 15.5 5 4 16.5ZM13.8 6.7l3.5 3.5M12 20h8"/></svg>',
  delete: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4.5 7h15M9 7V4.5h6V7m2.5 0-.8 13h-9L7 7m3 3v6m4-6v6"/></svg>',
  check: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m5 12.5 4.2 4.2L19 7"/></svg>',
  plus: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg>',
  sun: '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="3.5"/><path d="M12 2v2m0 16v2M4.93 4.93l1.42 1.42m11.3 11.3 1.42 1.42M2 12h2m16 0h2M4.93 19.07l1.42-1.42m11.3-11.3 1.42-1.42"/></svg>',
  moon: '<svg viewBox="0 0 24 24"><path d="M20.2 15.2A8.3 8.3 0 0 1 8.8 3.8 8.5 8.5 0 1 0 20.2 15.2Z"/></svg>',
  system: '<svg viewBox="0 0 24 24"><rect x="3.5" y="4.5" width="17" height="12" rx="2"/><path d="M8 20h8m-4-3.5V20"/></svg>',
  empty: '<svg viewBox="0 0 24 24"><path d="M5 5.5h14v13H9l-4 2v-15ZM8.5 10h7M8.5 14h5"/></svg>',
};

const listElement = document.querySelector("#entry-list");
const statusElement = document.querySelector("#status-message");
const dialog = document.querySelector("#editor-dialog");
const form = document.querySelector("#editor-form");

function t(key) {
  return translations[state.language][key];
}

function apiUrl(path, parameters = {}) {
  const query = new URLSearchParams(parameters);
  return `${API_ROOT}${path}?${query}`;
}

async function request(path, { method = "GET", parameters = {}, body } = {}) {
  const headers = { Authorization: `tma ${initData || ""}` };
  if (body !== undefined) headers["Content-Type"] = "application/json";
  const response = await fetch(apiUrl(path, parameters), {
    method,
    headers,
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  if (!response.ok) {
    const error = new Error(`HTTP ${response.status}`);
    error.status = response.status;
    throw error;
  }
  if (response.status === 204) return null;
  return response.json();
}

function setStatus(message = "", isError = false) {
  statusElement.textContent = message;
  statusElement.classList.toggle("error", isError);
}

function applyTheme() {
  const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  const activeTheme = state.theme === "system" ? (prefersDark ? "dark" : "light") : state.theme;
  document.documentElement.dataset.theme = activeTheme;
  const themeLabel = document.querySelector("#theme-label");
  const icon = document.querySelector(".theme-icon");
  themeLabel.textContent = t("theme")[state.theme];
  icon.outerHTML = icons[state.theme === "system" ? "system" : state.theme === "dark" ? "moon" : "sun"].replace(
    "<svg ", '<svg class="theme-icon" ',
  );
}

function applyLanguage() {
  const isArabic = state.language === "ar";
  document.documentElement.lang = state.language;
  document.documentElement.dir = isArabic ? "rtl" : "ltr";
  document.querySelector("#language-toggle").textContent = isArabic ? "EN" : "عربي";
  document.querySelector("#welcome-eyebrow").textContent = t("eyebrow");
  document.querySelector("#page-title").textContent = t("title");
  document.querySelector("#page-subtitle").textContent = t("subtitle");
  document.querySelector("#add-label").textContent = t("add");
  document.querySelector("#cancel-button").textContent = t("cancel");
  document.querySelector("#close-dialog").setAttribute("aria-label", t("cancel"));
  document.querySelector("#bottom-nav").setAttribute("aria-label", t("section").todos);
  applyTheme();
  renderNavigation();
  renderEntries();
  if (dialog.open) populateEditor();
}

function renderNavigation() {
  const navigation = document.querySelector("#bottom-nav");
  navigation.replaceChildren();
  for (const section of ["notes", "todos", "secrets"]) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = `nav-item${state.section === section ? " active" : ""}`;
    button.setAttribute("aria-current", state.section === section ? "page" : "false");
    button.innerHTML = `${icons[section]}<span>${t("nav")[section]}</span>`;
    button.addEventListener("click", () => selectSection(section));
    navigation.append(button);
  }
}

function createActionButton(icon, label, onClick) {
  const button = document.createElement("button");
  button.type = "button";
  button.className = "icon-button";
  button.setAttribute("aria-label", label);
  button.title = label;
  button.innerHTML = icons[icon];
  button.addEventListener("click", onClick);
  return button;
}

function renderEmptyState() {
  const template = document.querySelector("#empty-state-template");
  const empty = template.content.firstElementChild.cloneNode(true);
  empty.querySelector(".empty-icon").innerHTML = icons.empty;
  empty.querySelector("h3").textContent = t("emptyTitle")[state.section];
  empty.querySelector("p").textContent = t("emptyCopy")[state.section];
  listElement.append(empty);
}

function renderEntries() {
  document.querySelector("#section-title").textContent = t("section")[state.section];
  document.querySelector("#add-label").textContent = t("add");
  listElement.replaceChildren();

  if (!ownerId) {
    const empty = document.createElement("div");
    empty.className = "empty-state";
    empty.innerHTML = `<span class="empty-icon">${icons.secrets}</span><h3></h3><p></p>`;
    empty.querySelector("h3").textContent = t("title");
    empty.querySelector("p").textContent = t("missingTelegram");
    listElement.append(empty);
    document.querySelector("#add-button").disabled = true;
    return;
  }

  document.querySelector("#add-button").disabled = false;
  if (state.entries.length === 0) {
    renderEmptyState();
    return;
  }

  state.entries.forEach((entry, index) => {
    const meta = sectionMeta[state.section];
    const card = document.createElement("article");
    card.className = `entry-card${state.section === "todos" ? " todo-card" : ""}${entry.status ? " completed" : ""}`;
    card.style.animationDelay = `${Math.min(index, 8) * 30}ms`;

    if (state.section === "todos") {
      const check = document.createElement("button");
      check.type = "button";
      check.className = "todo-check";
      check.setAttribute("role", "checkbox");
      check.setAttribute("aria-checked", entry.status ? "true" : "false");
      check.setAttribute("aria-label", entry.status ? t("nav").todos : t("todoLabel"));
      if (entry.status) check.innerHTML = icons.check;
      check.addEventListener("click", () => setTodoStatus(entry, !Boolean(entry.status)));
      card.append(check);
    }

    const content = document.createElement("div");
    content.className = "entry-content";
    const title = document.createElement("p");
    title.className = "entry-title";
    title.textContent = state.section === "secrets" ? entry["title"] : entry[meta.valueKey];
    content.append(title);
    if (state.section === "secrets") {
      const secretValue = document.createElement("p");
      secretValue.className = "entry-body";
      secretValue.textContent = entry.password;
      content.append(secretValue);
    }
    card.append(content);

    const actions = document.createElement("div");
    actions.className = "card-actions";
    actions.append(createActionButton("edit", t("edit"), () => openEditor(entry)));
    actions.append(createActionButton("delete", t("delete"), () => deleteEntry(entry)));
    card.append(actions);
    listElement.append(card);
  });
}

async function loadEntries() {
  setStatus();
  if (!ownerId) {
    state.entries = [];
    renderEntries();
    return;
  }
  try {
    const rows = await request(sectionMeta[state.section].path);
    // The API currently serializes SQLite rows as arrays, while the UI uses
    // named fields. Convert each row here so display, edit, and delete share
    // the same stable object shape.
    const rowFields = {
      notes: ["id", "owner_id", "text"],
      todos: ["id", "owner_id", "task", "status"],
      secrets: ["id", "owner_id", "title", "password"],
    }[state.section];
    state.entries = rows.map((row) => {
      if (!Array.isArray(row)) return row;
      return Object.fromEntries(rowFields.map((field, index) => [field, row[index]]));
    });
    renderEntries();
  } catch (error) {
    state.entries = [];
    renderEntries();
    setStatus(`${t("loadError")} (${error.message})`, true);
    console.error("Could not load entries", error);
  }
}

async function selectSection(section) {
  state.section = section;
  renderNavigation();
  await loadEntries();
}

function createField({ name, label, placeholder, value = "", multiline = false }) {
  const group = document.createElement("label");
  group.className = "field-group";
  const labelElement = document.createElement("span");
  labelElement.className = "field-label";
  labelElement.textContent = label;
  const input = document.createElement(multiline ? "textarea" : "input");
  if (!multiline) input.type = "text";
  input.className = "text-field";
  input.name = name;
  input.placeholder = placeholder;
  input.value = value ?? "";
  input.required = true;
  group.append(labelElement, input);
  return group;
}

function populateEditor() {
  const editing = Boolean(state.editing);
  const section = state.section;
  document.querySelector("#dialog-eyebrow").textContent = t("section")[section];
  document.querySelector("#dialog-title").textContent = (editing ? t("dialogEdit") : t("dialogNew"))[section];
  document.querySelector("#save-button").textContent = editing ? t("update") : t("save");
  const fields = document.querySelector("#form-fields");
  fields.replaceChildren();

  if (section === "notes") {
    fields.append(createField({ name: "text", label: t("noteLabel"), placeholder: t("notePlaceholder"), value: state.editing?.text, multiline: true }));
  } else if (section === "todos") {
    fields.append(createField({ name: "task", label: t("todoLabel"), placeholder: t("todoPlaceholder"), value: state.editing?.task }));
  } else {
    fields.append(createField({ name: "title", label: t("secretTitleLabel"), placeholder: t("secretTitlePlaceholder"), value: state.editing?.title }));
    fields.append(createField({ name: "secret", label: t("secretValueLabel"), placeholder: t("secretValuePlaceholder"), value: state.editing?.password }));
  }
}

function openEditor(entry = null) {
  state.editing = entry;
  populateEditor();
  dialog.showModal();
  dialog.querySelector("input, textarea")?.focus();
}

async function saveEntry(event) {
  event.preventDefault();
  if (!form.reportValidity()) return;
  const values = Object.fromEntries(new FormData(form).entries());
  const meta = sectionMeta[state.section];
  const fields = state.section === "secrets"
    ? { title: values.title.trim(), secret: values.secret.trim() }
    : { [meta.valueKey]: values[meta.valueKey].trim() };
  if (Object.values(fields).some((value) => !value)) {
    setStatus(t("emptyField"), true);
    return;
  }
  const isEditing = Boolean(state.editing);
  const endpoint = isEditing ? meta.updatePath : meta.addPath;
  const parameters = isEditing ? { [meta.idKey]: state.editing.id } : {};
  try {
    await request(endpoint, {
      method: isEditing ? "PUT" : "POST",
      parameters,
      body: fields,
    });
    dialog.close();
    state.editing = null;
    await loadEntries();
  } catch (error) {
    setStatus(`${t("saveError")} (${error.message})`, true);
    console.error("Could not save entry", error);
  }
}

async function deleteEntry(entry) {
  if (!window.confirm(t("confirmDelete"))) return;
  const meta = sectionMeta[state.section];
  try {
    await request(meta.deletePath, {
      method: "DELETE",
      parameters: { [meta.idKey]: entry.id },
    });
    await loadEntries();
  } catch (error) {
    setStatus(`${t("deleteError")} (${error.message})`, true);
    console.error("Could not delete entry", error);
  }
}

async function setTodoStatus(entry, status) {
  try {
    await request("/set_todo_status", {
      method: "PUT",
      parameters: { todo_id: entry.id },
      body: { status },
    });
    await loadEntries();
  } catch (error) {
    setStatus(`${t("saveError")} (${error.message})`, true);
    console.error("Could not update task status", error);
  }
}

document.querySelector("#add-button").addEventListener("click", () => openEditor());
document.querySelector("#close-dialog").addEventListener("click", () => dialog.close());
document.querySelector("#cancel-button").addEventListener("click", () => dialog.close());
form.addEventListener("submit", saveEntry);
dialog.addEventListener("close", () => { state.editing = null; });
document.querySelector("#language-toggle").addEventListener("click", () => {
  state.language = state.language === "ar" ? "en" : "ar";
  localStorage.setItem("note-bot-language", state.language);
  applyLanguage();
});
document.querySelector("#theme-toggle").addEventListener("click", () => {
  const cycle = ["system", "light", "dark"];
  state.theme = cycle[(cycle.indexOf(state.theme) + 1) % cycle.length];
  localStorage.setItem("note-bot-theme", state.theme);
  applyTheme();
});
window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => {
  if (state.theme === "system") applyTheme();
});

if (webApp) {
  webApp.ready();
  webApp.expand();
}

applyLanguage();
loadEntries();
