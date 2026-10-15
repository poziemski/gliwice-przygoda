import streamlit as st


_BROWSER_SAVE_STORE = st.components.v2.component(
    "gliwice.browser_save_store",
    html="""
    <div aria-hidden="true" style="display:none"></div>
    """,
    js="""
    export default function (component) {
      const { data, parentElement, setStateValue } = component
      const storageKey = "gliwice-adventure-save-v1"

      if (!parentElement.__gliwiceSaveStoreHydrated) {
        try {
          const stored = window.localStorage.getItem(storageKey)
          const saveData = stored === null
            ? { version: 1, characters: [], adventures: {} }
            : JSON.parse(stored)
          parentElement.__gliwiceSaveStoreHydrated = true
          setStateValue("save_data", saveData)
          setStateValue("storage_error", "")
        } catch (error) {
          setStateValue("storage_error", `Nie udało się odczytać zapisu w przeglądarce: ${error}`)
        }
        return
      }

      if (data.ready) {
        try {
          window.localStorage.setItem(storageKey, JSON.stringify(data.save_data))
          if (data.storage_error) {
            setStateValue("storage_error", "")
          }
        } catch (error) {
          setStateValue("storage_error", `Nie udało się zapisać postępu w przeglądarce: ${error}`)
        }
      }
    }
    """,
)


def render_browser_save_store(save_data: dict | None, *, ready: bool):
    return _BROWSER_SAVE_STORE(
        key="browser-save-store",
        data={
            "save_data": save_data,
            "ready": ready,
            "storage_error": st.session_state.get("browser_storage_error", ""),
        },
        on_save_data_change=lambda: None,
        on_storage_error_change=lambda: None,
    )
