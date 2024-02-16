
#Functions to transform the perspective of the game.

def transform(self, x, y):
        """
        This is basically a function to make the game 2D or 3D, makes it easier to debug.
        Comment out the one you don't want to use.
        """
        #return self.transform_2D(x, y)
        return self.transform_perspective(x, y)

def transform_2D(self, x, y):
    """
    Leaves the perspective in 2D.
    """
    return int(x), int(y)

def transform_perspective(self, x, y):
    """
    Makes the perspective in 3D.
    """ 
    lin_y = y*self.perspective_point_y / self.height

    if lin_y > self.perspective_point_y:
        lin_y = self.perspective_point_y

    diff_x = x - self.perspective_point_x
    diff_y = self.perspective_point_y - lin_y
    factor_y = diff_y / self.perspective_point_y
    factor_y = pow(factor_y, 2)

    transform_x = self.perspective_point_x + diff_x * factor_y
    transform_y = self.perspective_point_y - factor_y * self.perspective_point_y

    return int(transform_x), int(transform_y)