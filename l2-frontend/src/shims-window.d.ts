export {};

declare global {
  interface Window {
    $: any
    Modernizr: any
    eds: any
    selectTextEl: (arg: any) => void
    okblink: (arg: any) => void
    clearselection: () => void
    set_instance: (arg: any) => void
    okmessage: (title: string, body: string | void) => void
    errmessage: (title: string, body: string | void) => void
    wrnmessage: (title: string, body: string | void) => void
    printResults: (pks: string[]) => void
    today: Date
    getFormattedDate: (d: Date) => string
  }
}
