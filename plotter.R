library(tidyverse)
library(ggokabeito)

distances <- read_csv('distances.csv')

distances |> 
  pivot_longer(
    cols = everything(),
    names_to = c('Construct', '.value'),
    names_pattern = "(.*)\\.(.*)"
  ) |> 
  pivot_longer(
    cols = c('ca', 'bond'),
    names_to = 'type',
    values_to = 'distance'
  ) |> 
  filter((type == 'ca' & distance > 3.75) | (type == 'bond')) |> 
  mutate(type = if_else(type == 'ca', 'Next CA', 'Carbonyl Carbon')) |> 
  ggplot(aes(x = distance)) +
  theme_minimal() +
  geom_density(aes(fill = Construct, y = ..scaled..)) +
  scale_fill_okabe_ito() +
  facet_grid(rows = vars(Construct), cols = vars(type), scales = 'free') +
  labs(
    x = 'Distance (A)',
    y = 'Scaled Density'
  )
ggsave('model-shifts.png', width = 8, height = 6, bg = 'white')

