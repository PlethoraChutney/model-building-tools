library(tidyverse)

data <- read_csv('3dfsc_results.csv')

directional <- data |> select(DirectionalHist) |> drop_na()
min_val = min(directional)
max_val = max(directional)

min_max_points = tibble(x = c(min_val, max_val), y = c(0, 0), shape = c(25, 24))
all_points = tibble(
  x = directional$DirectionalHist,
  y = 0,
  yend = -2 * 0.0075
)

histogram_binwidth = 0.0075

data |> 
  ggplot() +
  theme_minimal() +
  geom_histogram(
    aes(DirectionalHist, after_stat(count) / (100 * length(directional))),
    binwidth = histogram_binwidth,
    fill = '#CCCCCC'
  ) +
  geom_line(aes(GlobalX, GlobalY), linewidth = 1) +
  geom_segment(
    data = all_points,
    aes(x = x, y = y, xend = x, yend = yend),
    alpha = 0.3,
    position = position_jitter(width = histogram_binwidth/7, height = 0)
  ) +
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
ggsave('processed_3dfsc.pdf', width = 8, height = 4)
ggsave('processed_3dfsc.png', width = 8, height = 4, bg = 'white')
