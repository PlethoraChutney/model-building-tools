library(tidyverse)

data <- read_csv('processed-star.csv')

data |> 
  mutate(rlnAngleTilt = rlnAngleTilt - 90) |> 
  ggplot(aes(rlnAngleRot, rlnAngleTilt)) +
  theme_minimal() +
  geom_hex(binwidth = 6) +
  scale_fill_viridis_c(
    option = 'magma',
    trans = 'log',
    breaks = c(1, 10, 100, 1000)
  ) +
  scale_y_continuous(
    breaks = seq(-180, 180, by = 45)
  ) +
  scale_x_continuous(
    breaks = seq(-180, 180, by = 45)
  ) +
  coord_fixed() +
  labs(
    x = 'Azimuth (\u00B0)',
    y = 'Elevation (\u00B0)',
    fill = 'No. particles'
  )
ggsave('hexplot.pdf', width = 8, height = 4)
