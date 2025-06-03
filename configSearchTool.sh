#!/bin/bash

#=======================================================================================================
# Configuration File Search Tool
# Author: Chess W.
# Date: 2024-09-12
#
# This script searches for specific configurations in .ini files in the selected directory.
# It can search for specific sections, queries within sections, or queries across all files.
# Results are displayed based on the search criteria.
#
# Usage:
#   ./configSearchTool.sh [-m <model>] [-s <section>] [-z <query>] [-d <directory>] [-h]
#
# Arguments:
#   -m <model>   : Specify a device model (e.g., iPhone14,4)
#                  This will filter the search to only the specified model's config file.
#
#   -s <section> : Specify a section to search within (e.g., CameraRearPhoto)
#                  This will look for the specified section in the config files.
#
#   -z <query>   : Specify a query string to search for (e.g., "EnableTopBar = True")
#                  This will search for the exact string in the config files.
#                  If used with -s, it will search only within the specified section.
#                  If used alone, it will search across all sections in all files.
#
#   -d <directory> : Specify which directory to search in. Options:
#                    1 - DUT Parameters (/var/db/fusion/test_parameters/test_parameter_configs/dut_parameters)
#                    2 - DUT Configurations (/var/db/fusion/dut_configurations)
#                    If not specified, you will be prompted to choose.
#
#   -h           : Display this help message
#
# Search Behavior:
#   - When using only -m: Searches for the model's config file in the directory.
#   - When using only -s: Searches for the section in all config files in the directory, showing both found and missing files.
#   - When using only -z: Searches for the query in all config files in the directory, showing both found and missing files.
#   - When using -m and -s: Displays the content of the specified section in the specified model's config file.
#   - When using -z with -s: Searches for the query within the specified section in all config files.
#   - When using -z with -m: Searches for the query in the specified model's config file.
#   - When using -z with -m and -s: Searches for the query within the specified section in the specified model's config file.
#
# Examples:
#   1. Search for a query across all files in the directory:
#      ./configSearchTool.sh -z "EnableTopBar = True"
#
#   2. Search for a specific section in all files:
#      ./configSearchTool.sh -s Proximity
#
#   3. Display a specific section in a specific model's config:
#      ./configSearchTool.sh -m iPhone14,4 -s CameraRearPhoto
#
#   4. Search for a query in a specific model's config:
#      ./configSearchTool.sh -m iPhone14,4 -z "CamerasToSkip = 6"
#
#   5. Search in DUT Configurations directory:
#      ./configSearchTool.sh -d 2 -m iPhone14,4 -s CameraRearPhoto
#
# Output:
#   The script will display results based on the search criteria used.
#
# Note: This script requires read access to the directories mentioned above.
#
# Interactive Mode:
#   When run without arguments, the script enters interactive mode which allows
#   continuous searches without needing to restart the script. Press Ctrl+C at any
#   time to exit the interactive mode.
#=======================================================================================================

# Directory options
DUT_PARAMETERS=
DUT_CONFIGURATIONS=
LEGACY_PARAMETERS=
LEGACY_CONFIGURATIONS=
TRADES_PARAMETERS=


# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Function to print usage
# Print usage information and exit
# 
# This function prints the usage information of the script, including the
# arguments, examples, and search behavior. It is called when the script is
# invoked with the -h option or when no arguments are provided.
usage() {
    sed -n '/^# Usage:/,/^$/p' "$0" | sed 's/^# //'
    echo
    sed -n '/^# Arguments:/,/^$/p' "$0" | sed 's/^# //'
    echo
    sed -n '/^# Search Behavior:/,/^$/p' "$0" | sed 's/^# //'
    echo
    sed -n '/^# Examples:/,/^$/p' "$0" | sed 's/^# //'
    exit 1
}

# Function to display directory selection menu
select_directory() {
    echo -e "${BLUE}Please select the directory to search:${NC}"
    echo -e "${YELLOW}1)${NC} DUT Parameters ($DUT_PARAMETERS)"
    echo -e "${YELLOW}2)${NC} DUT Configurations ($DUT_CONFIGURATIONS)"
    echo -e "${YELLOW}3)${NC} Legacy Parameters ($LEGACY_PARAMETERS)"
    echo -e "${YELLOW}4)${NC} Legacy Configurations ($LEGACY_CONFIGURATIONS)"
    echo -e "${YELLOW}5)${NC} Trades Parameters ($TRADES_PARAMETERS)"
    echo -e "${YELLOW}6)${NC} Custom directory path"
    
    read -p "Enter your choice [1-6]: " dir_choice
    
    case $dir_choice in
        1) search_dir="$DUT_PARAMETERS" ;;
        2) search_dir="$DUT_CONFIGURATIONS" ;;
        3) search_dir="$LEGACY_PARAMETERS" ;;
        4) search_dir="$LEGACY_CONFIGURATIONS" ;;
        5) search_dir="$TRADES_PARAMETERS" ;;
        6) 
           read -p "Enter custom directory path: " custom_dir
           if [ -d "$custom_dir" ]; then
               search_dir="$custom_dir"
           else
               echo -e "${RED}Error: Directory does not exist.${NC}"
               exit 1
           fi
           ;;
        *) 
           echo -e "${RED}Invalid choice. Using default: DUT Parameters.${NC}"
           search_dir="$DUT_PARAMETERS"
           ;;
    esac
}

# Function to search for query
# Search for a query in a file, either in all sections or in a specific one.
#
# If a section is specified, the function will search for the query within that
# section only. If no section is specified, the function will search for the
# query across all sections in the file.
#
# The function returns the line number and the line of text that matches the
# query. If no match is found, the function returns nothing.
search_query() {
    local file=$1
    local query=$2
    local section=$3
    if [ -n "$section" ]; then
        awk -v section="$section" -v query="$query" '
            $0 ~ "\\[" section "\\]" {f=1; next}
            /^\[/ {f=0}
            f && $0 ~ query {print NR ":" $0; exit}
        ' "$file"
    else
        grep -n "$query" "$file"
    fi
}

# Main function to perform the search
perform_search() {
    local search_dir=$1
    local model=$2
    local section=$3
    local query=$4
    
    # Print search criteria
    echo
    echo -e "${BLUE}Search Parameters:${NC}"
    echo "----------------------------------------"
    if [ -n "$section" ]; then
        echo -e "Section: ${YELLOW}[$section]${NC}"
    fi
    if [ -n "$model" ]; then
        echo -e "Model: ${YELLOW}$model${NC}"
    fi
    if [ -n "$query" ]; then
        echo -e "Query: ${YELLOW}$query${NC}"
    fi
    echo -e "Directory: ${YELLOW}$search_dir${NC}"
    echo "----------------------------------------"
    
    # Process the directory
    files_searched=0
    files_with_match=0
    not_found_results=()
    found_results=()
    
    if [ -n "$model" ]; then
        files=("$search_dir/${model}.ini")
    else
        files=("$search_dir"/*.ini)
    fi
    
    # Check if directory exists and has .ini files
    if [ ! -d "$search_dir" ]; then
        echo -e "${RED}Error: Directory $search_dir does not exist.${NC}"
        return 1
    fi
    
    if [ -z "$(ls -A "$search_dir"/*.ini 2>/dev/null)" ] && [ -z "$model" ]; then
        echo -e "${RED}Error: No .ini files found in $search_dir${NC}"
        return 1
    fi
    
    # Process files
    for file in "${files[@]}"; do
        if [ -f "$file" ]; then
            ((files_searched++))
            filename=$(basename "$file")
            model_name="${filename%.*}"
            
            if [ -n "$query" ]; then
                query_result=$(search_query "$file" "$query" "$section")
                if [ -n "$query_result" ]; then
                    found_results+=("${GREEN}✓ $model_name: Query found${NC}")
                    found_results+=("$query_result")
                    found_results+=("----------------------------------------")
                    ((files_with_match++))
                else
                    not_found_results+=("${RED}✗ $model_name: Query not found${NC}")
                    not_found_results+=("----------------------------------------")
                fi
            elif [ -n "$section" ]; then
                if grep -q "\[$section\]" "$file"; then
                    found_results+=("${GREEN}✓ $model_name: Section [$section] found${NC}")
                    found_results+=("$(sed -n "/\[$section\]/,/^\[/p" "$file" | sed '$d')")
                    found_results+=("----------------------------------------")
                    ((files_with_match++))
                else
                    not_found_results+=("${RED}✗ $model_name: Section [$section] not found${NC}")
                    not_found_results+=("----------------------------------------")
                fi
            else
                found_results+=("${GREEN}✓ $model_name${NC}")
                # When searching only by model, display the file content
                found_results+=("$(cat "$file")")
                found_results+=("----------------------------------------")
                ((files_with_match++))
            fi
        elif [ -n "$model" ]; then
            echo -e "${RED}Error: File for model $model not found in $search_dir${NC}"
            return 1
        fi
    done
    
    # Print results
    echo
    echo -e "${BLUE}Search Results:${NC}"
    echo "----------------------------------------"
    
    # Only print found results
    if [ ${#found_results[@]} -gt 0 ]; then
        for result in "${found_results[@]}"; do
            echo -e "$result"
        done
    else
        # If nothing was found, show a single message rather than individual "not found" results
        if [ -n "$query" ]; then
            echo -e "${RED}Query \"$query\" not found in any searched files.${NC}"
        elif [ -n "$section" ]; then
            echo -e "${RED}Section [$section] not found in any searched files.${NC}"
        else
            echo -e "${RED}No matching files found.${NC}"
        fi
        echo "----------------------------------------"
    fi
    
    # Print summary
    echo -e "${BLUE}Summary:${NC}"
    echo "----------------------------------------"
    echo -e "Total files searched: ${YELLOW}$files_searched${NC}"
    echo -e "Files with match: ${YELLOW}$files_with_match${NC}"
    
    return 0
}

# Main script execution starts here

# Parse command line arguments
interactive_mode=false
show_exit_hint=false

# Check if script is run without arguments
if [ $# -eq 0 ]; then
    interactive_mode=true
fi

# Process command line arguments if not in interactive mode
if [ "$interactive_mode" = false ]; then
    while getopts ":m:s:z:d:h" opt; do
        case $opt in
            m) model="$OPTARG" ;;
            s) section="$OPTARG" ;;
            z) query="$OPTARG" ;;
            d) dir_option="$OPTARG" ;;
            h) usage ;;
            \?) echo -e "${RED}Invalid option -$OPTARG${NC}" >&2; usage ;;
        esac
    done
    
    # Set directory based on command line option
    if [ -n "$dir_option" ]; then
        case $dir_option in
            1) search_dir="$DUT_PARAMETERS" ;;
            2) search_dir="$DUT_CONFIGURATIONS" ;;
            3) search_dir="$LEGACY_PARAMETERS" ;;
            4) search_dir="$LEGACY_CONFIGURATIONS" ;;
            5) search_dir="$TRADES_PARAMETERS" ;;
            *)
               echo -e "${RED}Invalid directory option. Using default: DUT Parameters.${NC}"
               search_dir="$DUT_PARAMETERS"
               ;;
        esac
    else
        # Default to DUT Parameters if no directory specified
        search_dir="$DUT_PARAMETERS"
    fi
    
    # Perform the search
    if [ -z "$model" ] && [ -z "$section" ] && [ -z "$query" ]; then
        echo -e "${RED}Error: No search criteria provided.${NC}"
        usage
    else
        perform_search "$search_dir" "$model" "$section" "$query"
    fi
else
    # Interactive mode - loop through searches until user exits
    echo -e "${BLUE}Configuration Search Tool - Interactive Mode${NC}"
    echo -e "${YELLOW}Press Ctrl+C at any time to exit${NC}"
    
    while true; do
        # Reset variables for each iteration
        model=""
        section=""
        query=""
        search_dir=""
        
        # Show exit hint after first search
        if [ "$show_exit_hint" = true ]; then
            echo
            echo -e "${YELLOW}Press Ctrl+C to exit at any time${NC}"
        fi
        
        # Select directory
        select_directory
        
        # Prompt for search criteria
        echo
        echo -e "${BLUE}What would you like to search for?${NC}"
        echo -e "${YELLOW}1)${NC} Search by model"
        echo -e "${YELLOW}2)${NC} Search by section"
        echo -e "${YELLOW}3)${NC} Search by query string"
        echo -e "${YELLOW}4)${NC} Search by model and section"
        echo -e "${YELLOW}5)${NC} Advanced search (combine options)"
        
        read -p "Enter your choice [1-5]: " search_choice
        
        case $search_choice in
            1) 
                read -p "Enter model name (e.g., iPhone14,4): " model
                ;;
            2)
                read -p "Enter section name (e.g., CameraRearPhoto): " section
                ;;
            3)
                read -p "Enter query string (e.g., EnableTopBar = True): " query
                ;;
            4)
                read -p "Enter model name (e.g., iPhone14,4): " model
                read -p "Enter section name (e.g., CameraRearPhoto): " section
                ;;
            5)
                read -p "Enter model name (leave empty to skip): " model_input
                if [ -n "$model_input" ]; then
                    model="$model_input"
                fi
                
                read -p "Enter section name (leave empty to skip): " section_input
                if [ -n "$section_input" ]; then
                    section="$section_input"
                fi
                
                read -p "Enter query string (leave empty to skip): " query_input
                if [ -n "$query_input" ]; then
                    query="$query_input"
                fi
                ;;
            *)
                echo -e "${RED}Invalid choice. Please select from options 1-5.${NC}"
                continue
                ;;
        esac
        
        # Check if at least one search argument is provided
        if [ -z "$model" ] && [ -z "$section" ] && [ -z "$query" ]; then
            echo -e "${RED}Error: No search criteria provided.${NC}"
            continue
        fi
        
        # Perform the search
        perform_search "$search_dir" "$model" "$section" "$query"
        
        # Set flag to show exit hint in subsequent iterations
        show_exit_hint=true
        
        echo
        echo -e "${BLUE}--------------------------------------------------${NC}"
        echo -e "${YELLOW}Starting new search... (Press Ctrl+C to exit)${NC}"
        echo -e "${BLUE}--------------------------------------------------${NC}"
    done
fi
