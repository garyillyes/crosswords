import random

class CrosswordGenerator:
    def __init__(self):
        self.grid = {}  # Map (x, y) -> char
        self.placed_words = [] # List of {word, clue, x, y, direction}
        self.height = 0
        self.width = 0

    def generate(self, word_data, max_attempts=50):
        """
        word_data: List of dicts {'word': 'EXAMPLE', 'clue': '...'}
        """
        # Sort by length, longest first usually helps framing
        word_data = sorted(word_data, key=lambda x: len(x['word']), reverse=True)
        
        best_grid = None
        best_score = -1

        for attempt in range(max_attempts):
            self.grid = {}
            self.placed_words = []
            
            # Place first word in the middle
            first = word_data[0]
            self._place_word(first['word'], first['clue'], first.get('definition', ''), first.get('source_url', ''), 0, 0, 'horizontal')
            
            # Try to fit the rest
            shuffled_remainder = word_data[1:]
            random.shuffle(shuffled_remainder)
            
            for item in shuffled_remainder:
                self._try_fit_word(item['word'], item['clue'], item.get('definition', ''), item.get('source_url', ''))
            
            if len(self.placed_words) > best_score:
                best_score = len(self.placed_words)
                best_grid = (self.grid.copy(), self.placed_words[:])
        
        # Restore best
        if best_grid:
            self.grid, self.placed_words = best_grid
            self._normalize_coordinates()
            return self._export()
        return None

    def _place_word(self, word, clue, definition, source_url, x, y, direction):
        for i, char in enumerate(word):
            cx, cy = (x + i, y) if direction == 'horizontal' else (x, y + i)
            self.grid[(cx, cy)] = char
        
        self.placed_words.append({
            'word': word,
            'word': word,
            'clue': clue,
            'definition': definition,
            'source_url': source_url,
            'startX': x,
            'startY': y,
            'direction': direction,
            'length': len(word)
        })

    def _try_fit_word(self, word, clue, definition, source_url):
        possible_moves = []
        
        # Find all intersections with existing grid
        for i, char in enumerate(word):
            for (gx, gy), gchar in self.grid.items():
                if char == gchar:
                    # Potential intersection found
                    # If existing is horizontal, we must be vertical, and vice versa
                    # However, strictly determining existing direction is hard per cell.
                    # We just try both orthogonal directions relative to the match.
                    
                    # Try Vertical through this point
                    # The word's ith char is at gx, gy. So start is gx, gy - i
                    if self._can_place(word, gx, gy - i, 'vertical'):
                        possible_moves.append((gx, gy - i, 'vertical'))
                    
                    # Try Horizontal
                    if self._can_place(word, gx - i, gy, 'horizontal'):
                        possible_moves.append((gx - i, gy, 'horizontal'))

        if possible_moves:
            x, y, direct = random.choice(possible_moves)
            self._place_word(word, clue, definition, source_url, x, y, direct)
            return True
        return False

    def _can_place(self, word, x, y, direction):
        # 1. Check bounds/overlap conflicts
        # 2. Check "tight grouping" (don't place words immediately adjacent parallel)
        
        for i, char in enumerate(word):
            cx, cy = (x + i, y) if direction == 'horizontal' else (x, y + i)
            
            # If cell occupied, must match
            if (cx, cy) in self.grid:
                if self.grid[(cx, cy)] != char:
                    return False
            else:
                # Cell is empty. Check immediate neighbors (pseudo-black squares)
                # We cannot touch another word parallel-y unless it's a cross point
                neighbors = [
                    (cx+1, cy), (cx-1, cy), (cx, cy+1), (cx, cy-1)
                ]
                
                # Filter out the cells that will be occupied by THIS word
                # (Prev, Next in sequence)
                ignore = []
                if direction == 'horizontal':
                    ignore = [(cx-1, cy), (cx+1, cy)]
                else:
                    ignore = [(cx, cy-1), (cx, cy+1)]
                
                for nx, ny in neighbors:
                    if (nx, ny) in ignore: continue
                    if (nx, ny) in self.grid:
                        return False # Touching another word incorrectly
                        
        # Check start and end constraints (word shouldn't extend existing words)
        if direction == 'horizontal':
            if (x-1, y) in self.grid or (x+len(word), y) in self.grid: return False
        else:
            if (x, y-1) in self.grid or (x, y+len(word)) in self.grid: return False
            
        return True

    def _normalize_coordinates(self):
        if not self.grid: return
        min_x = min(k[0] for k in self.grid.keys())
        min_y = min(k[1] for k in self.grid.keys())
        max_x = max(k[0] for k in self.grid.keys())
        max_y = max(k[1] for k in self.grid.keys())

        # Shift everything to 0,0
        self.width = (max_x - min_x) + 1
        self.height = (max_y - min_y) + 1
        
        new_words = []
        for w in self.placed_words:
            w['startX'] -= min_x
            w['startY'] -= min_y
            new_words.append(w)
        self.placed_words = new_words

    def _export(self):
        return {
            'width': self.width,
            'height': self.height,
            'words': self.placed_words,
            'generated_at_utc': 'ISO_DATE_PLACEHOLDER'
        }