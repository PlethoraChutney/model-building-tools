library(tidyverse)

data <- read_csv('3dfsc_results.csv')

directional <- data |> select(DirectionalHist) |> drop_na()
min_val = min(directional)
max_val = max(directional)

min_max_points = tibble(x = c(min_val, max_val), y = c(0, 0), shape = c(25, 24))

data |> 
  ggplot() +
  theme_minimal() +
  geom_histogram(
    aes(DirectionalHist, after_stat(count) / (100 * length(directional))),
    binwidth = 0.005,
    fill = '#CCCCCC'
  ) +
  geom_line(aes(GlobalX, GlobalY)) +
  geom_point(data = min_max_points, aes(x, y, shape = shape)) +
  scale_x_continuous(
    breaks = c(0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6),
    labels = c('DC', '10', '5', '3.3', '2.5', '2', '1.2')
  ) +
  scale_y_continuous(
    sec.axis = sec_axis(
      trans = ~ . * 100,
      name = 'Percentage of per-angle FSC (%)'
    )
  ) +
  scale_shape_identity() +
  labs(
    x = 'Resolution (\u00C5)',
    y = 'Global FSC'
  )
