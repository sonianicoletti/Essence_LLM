# Load required packages
library(ggplot2)
library(showtext)

# Enable showtext and add Poppins font
font_add_google("Poppins", "poppins")
font_add_google("Montserrat", "montserrat")
showtext_auto()

# Define the data
data <- data.frame(
  Category = c("Essence Kernel and Language", "Essence Cards", 
               "Essence Games", "Essentializing Software Engineering Practices"),
  Count = c(5, 3, 3, 11)
)

# Specify custom colors for each category
custom_colors <- c("Essence Kernel and Language" = "#9bb0ffff",  # Light Red
                   "Essence Cards" = "#ff96b1ff",                # Light Blue
                   "Essence Games" = "#8ae6bfff",                # Light Green
                   "Essentializing Software Engineering Practices" = "#ffb59aff") # Light Orange

# Create the pie chart
pie_chart <- ggplot(data, aes(x = "", y = Count, fill = Category)) +
  geom_bar(stat = "identity", width = 1, color = "white") +
  coord_polar("y", start = 0) +  # Start at 0 for clockwise direction
  labs(title = "", x = NULL, y = NULL) +
  theme_void() +  # Remove unnecessary gridlines and axes
  scale_fill_manual(values = custom_colors) +  # Apply custom colors
  theme(
    plot.title = element_text(hjust = 0.5, face = "bold", size = 60, family = "montserrat", color = "#1a1e2d"), # Larger title
    legend.text = element_text(size = 65, family = "poppins", color = "#1a1e2d"),  # Larger legend text
    legend.title = element_blank(),
    legend.key.size = unit(1, "cm"),  # Adjust legend key size
    legend.spacing.y = unit(0.8, "cm"),  # Adjust spacing between legend items
    plot.background = element_rect(fill = "white", color = NA)  # Set background to white
  ) +
  guides(fill = guide_legend(reverse = TRUE))  # Reverse the legend order to match the counts


# Save the chart as an image
ggsave("document_distribution_pie_chart.png", plot = pie_chart, width = 12, height = 4.5, dpi = 300, bg = "white")
