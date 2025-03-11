# Load required libraries
library(ggplot2)
library(ggpattern)  # Allows pattern fills in ggplot2

# Data for the pie chart
data <- data.frame(
  category = c("ESE Practices", "Essence Kernel", "Essence Games", "Essence Cards"),
  value = c(50, 22.7, 13.6, 13.6),
  pattern = c("stripe", "dot", "crosshatch", "grid")  # Different patterns
)

# Create the pie chart
ggplot(data, aes(x = "", y = value, fill = category, pattern = pattern)) +
  geom_bar(stat = "identity", width = 1, colour = "black", position = "stack") +
  coord_polar(theta = "y") +
  scale_fill_manual(values = c("white", "white", "white", "white")) +  # No colours
  scale_pattern_manual(values = c("stripe", "dot", "crosshatch", "grid")) + # Apply patterns
  theme_minimal() +
  theme(
    axis.text = element_blank(),
    axis.ticks = element_blank(),
    panel.grid = element_blank(),
    legend.title = element_blank()
  ) +
  labs(title = "Distribution of Essence-Related Documents")
