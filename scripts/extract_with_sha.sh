#!/bin/bash
set -eo pipefail

# Configure color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration paths - modify as needed
COMPRESSED_DIR="Aviation-HV-UAV_Split_Compressed"   # Directory containing archives
DEST_DIR="Aviation-HV-UAV_Split"                    # Extraction target directory
MERGED_DIR="Aviation-HV-UAV-merged"                 # Final merged directory

# Check for required tools
check_dependencies() {
    local dependencies=("sha256sum" "tar" "zstd" "xz" "gzip" "df" "du")
    for dep in "${dependencies[@]}"; do
        if ! command -v "$dep" &> /dev/null; then
            echo -e "${RED}Error: Required tool $dep not found. Please install it first.${NC}"
            exit 1
        fi
    done
}

# Check available disk space
check_disk_space() {
    local required_space=$1
    local target_dir=$2

    # Get available space in target partition (KB)
    local available_space=$(df -P "$target_dir" | tail -1 | awk '{print $4}')

    # Convert to GB for display
    local required_gb=$((required_space / 1024 / 1024))
    local available_gb=$((available_space / 1024 / 1024))

    if [ "$available_space" -lt "$required_space" ]; then
        echo -e "${RED}Error: Insufficient disk space!${NC}"
        echo -e "Need at least ${required_gb}GB, currently available ${available_gb}GB in $(df -P "$target_dir" | tail -1 | awk '{print $6}')"
        exit 1
    fi
}

# Show script usage help
show_help() {
    echo "Usage: $0 [options]"
    echo "Script for processing archives and merging contents"
    echo
    echo "Options:"
    echo "  -c, --cleanup    Clean up extraction directory after processing (keeps merged directory)"
    echo "  -h, --help       Show this help message"
    echo
    echo "Configuration paths:"
    echo "  Archive directory: $COMPRESSED_DIR"
    echo "  Extraction directory: $DEST_DIR"
    echo "  Merged directory: $MERGED_DIR"
}

# Main function
main() {
    local cleanup=false

    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -c|--cleanup)
                cleanup=true
                shift
                ;;
            -h|--help)
                show_help
                exit 0
                ;;
            *)
                echo -e "${RED}Error: Unknown option $1${NC}"
                show_help
                exit 1
                ;;
        esac
    done

    # Check dependencies
    check_dependencies

    # Create directories
    echo -e "${BLUE}Creating necessary directories...${NC}"
    mkdir -p "$COMPRESSED_DIR" "$DEST_DIR" "$MERGED_DIR"

    # Check if there are any archive files
    if [ -z "$(ls -A "$COMPRESSED_DIR"/*.tar.* 2>/dev/null)" ]; then
        echo -e "${YELLOW}Warning: No .tar.* archives found in $COMPRESSED_DIR${NC}"
        exit 0
    fi

    # Estimate required space (2x total archive size as safety margin)
    local total_size=$(du -c "$COMPRESSED_DIR"/*.tar.* 2>/dev/null | tail -1 | awk '{print $1}')
    local required_space=$((total_size * 2 * 1024))  # Convert to KB and double

    # Check target partition space
    check_disk_space "$required_space" "$DEST_DIR"

    # Process each archive
    local archive_count=$(ls -1 "$COMPRESSED_DIR"/*.tar.* 2>/dev/null | wc -l)
    local current_archive=0

    echo -e "\n${BLUE}Starting processing of $archive_count archives...${NC}"
    for archive in "$COMPRESSED_DIR"/*.tar.*; do
        # Skip non-existent files (handles wildcard no-matches)
        [ -e "$archive" ] || continue

        current_archive=$((current_archive + 1))
        filename=$(basename "$archive")

        echo -e "\n${BLUE}=== Processing $filename ($current_archive/$archive_count) ===${NC}"

        # Verify file
        sha_file="$archive.sha256"
        if [ -f "$sha_file" ]; then
            echo -n "Verifying $filename ... "
            if sha256sum -c "$sha_file" >/dev/null 2>&1; then
                echo -e "${GREEN}? Verification passed${NC}"
            else
                echo -e "${RED}? Verification failed, skipping this file${NC}"
                continue
            fi
        else
            echo -e "${YELLOW}?? No checksum file $sha_file found, skipping verification${NC}"
        fi

        # Extract file
        echo -n "Extracting $filename to $DEST_DIR ... "
        case "$archive" in
            *.tar.zst)
                if zstd -d -c "$archive" | tar -x -C "$DEST_DIR" >/dev/null 2>&1; then
                    echo -e "${GREEN}Completed${NC}"
                else
                    echo -e "${RED}Failed${NC}"
                    exit 1
                fi
                ;;
            *.tar.xz)
                if tar -xJf "$archive" -C "$DEST_DIR" >/dev/null 2>&1; then
                    echo -e "${GREEN}Completed${NC}"
                else
                    echo -e "${RED}Failed${NC}"
                    exit 1
                fi
                ;;
            *.tar.gz)
                if tar -xzf "$archive" -C "$DEST_DIR" >/dev/null 2>&1; then
                    echo -e "${GREEN}Completed${NC}"
                else
                    echo -e "${RED}Failed${NC}"
                    exit 1
                fi
                ;;
            *)
                echo -e "${YELLOW}?? Unsupported file format, skipping $filename${NC}"
                continue
                ;;
        esac
    done

    # Merge files
    echo -e "\n${BLUE}Starting file merging to $MERGED_DIR ...${NC}"
    if [ -z "$(ls -A "$DEST_DIR" 2>/dev/null)" ]; then
        echo -e "${RED}Error: Extraction directory $DEST_DIR is empty, cannot merge${NC}"
        exit 1
    fi

    # Create directory structure in merged directory
    find "$DEST_DIR" -type d -exec mkdir -p "$MERGED_DIR"/{} \; 2>/dev/null

    # Move files, handling potential filename conflicts
    find "$DEST_DIR" -type f -print0 | while IFS= read -r -d '' file; do
        rel_path="${file#$DEST_DIR/}"
        target="$MERGED_DIR/$rel_path"

        if [ -f "$target" ]; then
            # Handle file conflicts: add numeric suffix
            base=$(basename "$target")
            dir=$(dirname "$target")
            ext="${base##*.}"
            name="${base%.*}"
            counter=1

            # Find available filename
            while [ -f "$dir/$name-$counter.$ext" ]; do
                counter=$((counter + 1))
            done

            target="$dir/$name-$counter.$ext"
            echo -e "${YELLOW}?? File $rel_path already exists, renamed to ${name}-${counter}.${ext}${NC}"
        fi

        mv "$file" "$target"
    done

    # Clean up empty directories
    find "$DEST_DIR" -type d -empty -delete 2>/dev/null

    # Optional cleanup
    if [ "$cleanup" = true ]; then
        echo -e "\n${BLUE}Cleaning up temporary files...${NC}"
        rm -rf "$DEST_DIR"
    fi

    # Show final statistics
    local merged_files=$(find "$MERGED_DIR" -type f | wc -l)
    local merged_size=$(du -sh "$MERGED_DIR" | awk '{print $1}')

    echo -e "\n${GREEN}All operations completed successfully!${NC}"
    echo -e "Total merged files: $merged_files"
    echo -e "Total merged size: $merged_size"
    echo -e "Files location: $(realpath "$MERGED_DIR")"
}

# Start main function
main "$@"
