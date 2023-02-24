def overlap(box, xcoord):
    # box is ymin,xmin,ymax,xmax
    # xcoord is an xcoord for all y
    if xcoord > box[1] and xcoord < box[3]:
        return True 
    return False