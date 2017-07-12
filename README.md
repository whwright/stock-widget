stock-widget
============

A basic stock ticker widget for awesome WM.

![stock widget](./screenshot.png)

Insiration taken from [deficient](https://github.com/deficient) widgets.

### Installation

Put `stock-widget.lua` and `get_stock_price.py` in your awesome config folder.

Then, in your rc.lua:

```lua
local stock_widget = require("stock-widget")
stock = stock_widget({symbol = "NYSE:HD"})
-- add the widget to your wibox
{
    -- right widgets
    ...
    stock.widget
    ...
}
```

### Config

The text can be configured with the following properties

```lua
stock_widget({
    text_format = "${symbol_color_on}${symbol}${symbol_color_off} ${price_color_on}\$${price}${price_color_off} ${change_color_on}${change}%${change_color_off}",
    symbol_color = "white",
    price_color = nil,
    gain_color = "green",
    loss_color = "red"
})
```
