library(tidyverse)

data <- read_csv('processed_table.csv')

data |> 
  ggplot(aes(res, FSC)) +
  theme_minimal() +
  theme(
    legend.position = 'top'
  ) +
  geom_hline(
    yintercept = 0.143,
    color = '#AAAAAA',
    linetype = 'dashed'
  ) +
  scale_color_manual(values = c('#0077BB', '#EE99AA')) +
  geom_line(aes(color = Table)) +
  expand_limits(y = 1) +
  scale_x_continuous(
    breaks = c(0, 1/10, 1/5, 1/3, 1/2, 1, 2),
    labels = c('DC', '10', '5', '3', '2', '1', '0.5'),
    minor_breaks = 1/c(7.5, 4, 2.5, 1.5)
  ) +
  scale_y_continuous(minor_breaks = NULL) +
  labs(
    x = 'Resolution (\u00C5)',
    y = 'Model-Map FSC',
    color = NULL
  )
ggsave('model-map.pdf', width = 8, height = 4)
