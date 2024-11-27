# Load required packages
library(ggplot2)
library(readr)
library(dplyr)
library(showtext)

# Enable showtext and add fonts
font_add_google("Poppins", "poppins")
font_add_google("Montserrat", "montserrat")
showtext_auto()

# Load the CSV file
csv_file <- 'scores_human_avg.csv'  # Replace with your file path
df_human_avg <- read_csv(csv_file)

# Ensure the required columns are present
required_columns <- c('relevance_coach', 'accuracy_coach', 'completeness_coach', 
                      'relevance_gpt', 'accuracy_gpt', 'completeness_gpt', 'question_type')

missing_columns <- setdiff(required_columns, colnames(df_human_avg))
if (length(missing_columns) > 0) {
  stop(paste("The CSV file is missing the following columns:", paste(missing_columns, collapse = ", ")))
}

# Manually set the `question_type` for the first row if missing
if (is.na(df_human_avg[1, 'question_type'])) {
  df_human_avg[1, 'question_type'] <- 'Overall'
}

# Define metrics
metrics <- c('relevance', 'accuracy', 'completeness')

# Define question types
question_types <- c('overall', 'information', 'decision-making', 'translation')

# Customizable colors for the models
custom_colors <- c("Essence Coach" = "#ffb59aff", "GPT-4o" = "#9bb0ffff")

# Create a bar plot for each question type
for (qtype in question_types) {
  # Filter the data for the current question type
  row <- df_human_avg %>% filter(tolower(question_type) == qtype)
  
  if (nrow(row) > 0) {
    coach_scores <- unlist(row[, paste0(metrics, "_coach")])
    gpt_scores <- unlist(row[, paste0(metrics, "_gpt")])
    
    # Prepare the data for plotting
    plot_data <- data.frame(
      metric = rep(c('Relevance', 'Accuracy', 'Completeness'), 2),
      score = c(coach_scores, gpt_scores),
      model = rep(c("Essence Coach", "GPT-4o"), each = length(metrics))
    )
    
    # Create the bar plot
    p <- ggplot(plot_data, aes(x = metric, y = score, fill = model, group = model)) +
      geom_bar(stat = "identity", position = position_dodge(width = 0.8), width = 0.8) +  # Adjusted to avoid overlap
      geom_text(aes(label = sprintf("%.3f", score)), position = position_dodge(width = 0.8), vjust = -0.5, size = 14, family = "poppins", color = "#1a1e2d") +
      labs(
        title = paste(toupper(substring(qtype, 1, 1)), substring(qtype, 2), " Scores Comparison", sep = ""),
        x = NULL,
        y = "Scores"
      ) +
      theme_minimal() +
      theme(
        text = element_text(size = 70, family = "poppins", color = "#1a1e2d"),
        axis.text.x = element_text(size = 70, family = "poppins", color = "#1a1e2d"),
        axis.text.y = element_text(size = 70, family = "poppins", color = "#1a1e2d"),
        plot.title = element_text(size = 80, hjust = 0.5, family = "montserrat", face = "bold", color = "#1a1e2d"),
        legend.text = element_text(size = 70, family = "poppins", color = "#1a1e2d"),
        legend.title = element_blank(),
        legend.position = "top",
        panel.background = element_rect(fill = "white"),  # White background
        plot.background = element_rect(fill = "white")    # White background
      ) +
      scale_fill_manual(values = custom_colors) +
      ylim(0, 3)  # Set the y-axis limit to 3
    
    # Save and show the plot
    output_image <- paste0('scores_comparison_', qtype, '.png')
    ggsave(output_image, plot = p, dpi = 300, width = 8, height = 6, bg = "transparent")
    print(paste("Bar plot for", qtype, "saved as an image:", output_image))
  } else {
    print(paste("No data found for question type", qtype, ". It will be skipped."))
  }
}
