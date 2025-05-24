import pygame

class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		self.is_hovering = False # Track hover state

		if self.image is None:
			# If no image is provided, create a surface for the text
			text_surface = self.font.render(self.text_input, True, self.base_color)
			# Create a basic background surface for the text for better hitbox
			# You might want to customize the size/padding later
			self.image = pygame.Surface((text_surface.get_width() + 40, text_surface.get_height() + 20), pygame.SRCALPHA)
			# Initial fill for the background if needed (e.g., a semi-transparent color)
			# self.image.fill((50, 50, 50, 100)) # Example: dark grey with transparency
			self.image.blit(text_surface, (20, 10)) # Center text on the surface

		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		# Recalculate text_rect to be centered relative to the button's center after image/surface creation
		self.text_rect = self.text.get_rect(center=self.rect.center)

	def update(self, screen):
		# Draw the button image (or background surface)
		screen.blit(self.image, self.rect)
		# Draw the text centered on the button
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		# Check for hover and update text color
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			if not self.is_hovering:
				self.text = self.font.render(self.text_input, True, self.hovering_color)
				self.is_hovering = True
		else:
			if self.is_hovering:
				self.text = self.font.render(self.text_input, True, self.base_color)
				self.is_hovering = False

		# Optional: Change background on hover if image is None
		# If you uncomment this, you might want to adjust the surface creation in __init__
		# if self.image is not None and not isinstance(self.image, pygame.Surface): # Only do this if the image is a loaded image, not our created surface
		#     pass # Don't change background for loaded images
		# elif self.is_hovering and isinstance(self.image, pygame.Surface):
		#     # Redraw the background surface with a highlight
		#     text_surface = self.font.render(self.text_input, True, self.hovering_color) # Render with hover color for positioning
		#     self.image.fill((50, 50, 50, 150)) # Example: slightly darker background on hover
		#     self.image.blit(text_surface, (10, 10)) # Center text
		# elif isinstance(self.image, pygame.Surface): # Not hovering, reset background
		#     text_surface = self.font.render(self.text_input, True, self.base_color) # Render with base color for positioning
		#     self.image.fill((50, 50, 50, 100)) # Example: original background
		#     self.image.blit(text_surface, (10, 10)) # Center text