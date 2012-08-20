if smallest_window_title == float('inf'):
            Boost_title = 1
        elif smallest_window_title == len(query_vector):
            Boost_title = self.B
        else:
            Boost_title = (1 + 1.0/smallest_window_title) * self.B 
        
        if smallest_window_body == float('inf'):
            Boost_body = 1
        elif smallest_window_body == len(query_vector):
            Boost_body = self.B
        else:
            Boost_body = (1 + 1.0/smallest_window_title) * self.B 
        
        if smallest_window_anchor == float('inf'):
            Boost_anchor = 1
        elif smallest_window_anchor == len(query_vector):
            Boost_anchor = self.B
        else:
            Boost_anchor = (1 + 1.0/smallest_window_title) * self.B