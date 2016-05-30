import os, sys
import pygame
import resources

#The Console class will display the "console" object on the screen
#
class Console:
  
  def __init__(self, screen):
    self.font = pygame.font.SysFont('calibri', 30)
    self.screen = screen
    self.console_img = resources.all_sprites['console.png']
    self.message_list = []
    self.message_list_max_size = 10
    self.console_pos = (628, 30)
    self.color = pygame.Color(255, 255, 255)
	
  def draw(self):
    self.screen.blit(self.console_img, self.console_pos)
    for m in range(len(self.message_list)):
      self.console_output = self.font.render(self.message_list[m], True, self.color)
      self.screen.blit (self.console_output, (self.console_pos[0] + 5, self.console_pos[1] + 10 + (self.font.get_linesize() * m)))
			
  #get_message grabs the next object in a message queue
  def get_message(self, incoming_message_queue):
    if len(incoming_message_queue) != 0:
      time = '[' + '{:02d}:{:02d}'.format(resources.time.hour, resources.time.minute) + '] '
      message_in_queue = incoming_message_queue.pop(0)
      event = message_in_queue[2]
      message = time

      if type(event) == int:
        damage = event
        message += message_in_queue[0] + " has attacked " + message_in_queue[1] + " for " + str(damage)
  
      if type(event) == str:
        if event == "Missed":
          message += message_in_queue[0] + " missed."
        if event == "Damaged" or event == "Flavor":
          message += message_in_queue[3]
      
      multiline = self.sanitize(message)

      for msg in multiline:
        self.message_list.append(msg)
      
      while len(self.message_list) >= self.message_list_max_size:
        self.message_list.pop(0)


  def sanitize(self, msg):
    if (self.font.size(msg))[0] < 630:
      return [msg]
    
    final_messages = []
    while True:
      message = msg.split()
      prevMsg = ""
      for m in range(len(message)+1):
        thisMsg = " ".join(message[:m])
        thisMsg = thisMsg.strip()
        if (self.font.size(thisMsg))[0] >= 630:
          final_messages.append(prevMsg)
          msg = " ".join(message[m-1:])
          break
        else:
          prevMsg = thisMsg
      if (self.font.size(msg))[0] < 630:
        if msg != "":
          final_messages.append(msg)
        break
    return final_messages

