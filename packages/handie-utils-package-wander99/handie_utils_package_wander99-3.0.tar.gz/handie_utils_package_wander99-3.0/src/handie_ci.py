# © 2022 George Fenn
# V1 This module will provide a common interface for simple
# text input like what the summit and park lookups need.
# V2 Added a method call to the ci_inp TextField to give
# the keyboard focus in that field for input. 

import ui
import dialogs

def ci_init(title):
  global vi
  
  vi=ui.load_view('handie_ci_ui')
  vi.name=title
  vi.ci_done_button_pressed=False
  vi.ci_text_input=''
  
  return vi
    
def ci_done_button_pressed(sender):
  vi.close()
  vi.ci_done_button_pressed=True

def ci_text_received(sender):
  vi_input = sender.superview['ci_inp']
  vi.ci_text_input=vi_input.text
  vi_input.text=''
    
def ci_view_present():
  
  vi_focus=vi['ci_inp']
  vi_focus.begin_editing()
  if min(ui.get_screen_size()) >= 768:
    # iPad
    vi.frame = (0, 0, 360, 400)
    vi.present('sheet')
  else:
    # iPhone
    vi.present(orientations=['portrait'])
  vi.wait_modal()
    
def main():
  tt=' Testing'
  vi=ci_init(tt)
  ci_view_present()
  dd1=vi.ci_text_input
  vi.ci_text_input=''
  if dd1 == '':
    i = dialogs.alert(' No input received! ','','OK',hide_cancel_button=True)
  else:
    i = dialogs.alert(f' Input received :{dd1}  ','','OK',hide_cancel_button=True)
  if vi.ci_done_button_pressed == True:
    vi.close()
    i = dialogs.alert(' We are done! ','','OK',hide_cancel_button=True)
  
if __name__ == "__main__":
  main()
