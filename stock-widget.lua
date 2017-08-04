local wibox = require("wibox")
local awful = require("awful")
awful.util = require("awful.util")
local os = require("os")
local naughty = require("naughty")


local function color_tags(color)
    if color
    then return '<span color="' .. color .. '">', '</span>'
    else return '', ''
    end
end

local function substitute(template, context)
    if type(template) == "string" then
        return (template:gsub("%${([%w_]+)}", function(key)
            return tostring(context[key] or "Err!")
        end))
    else
        -- function / functor:
        return template(context)
    end
end


local stock_widget = {}

function stock_widget:new(args)
    return setmetatable({}, {__index = self}):init(args)
end

function stock_widget:init(args)
    if args.symbol == nil then
        error("symbol is require")
    end

    self.symbol = args.symbol
    self.widget = wibox.widget.textbox()

    self.text_format = args.text_format or (
        "${symbol_color_on}${symbol}${symbol_color_off} ${price_color_on}\$${price}${price_color_off} ${change_color_on}${change}%${change_color_off}")
    self.symbol_color = args.symbol_color or "white"
    self.price_color = args.price_color or nil
    self.gain_color = args.gain_color or "green"
    self.loss_color = args.loss_color or "red"

    self.get_stock_price_location = args.get_stock_price_location
    if self.get_stock_price_location == nil then
        local home = os.getenv("HOME")
        local base_config_location = home .. "/.config/awesome"
        local sub_module_location = home .. "/.config/awesome/stock-widget"
        if awful.util.file_readable(base_config_location .. "/get_stock_price.py") then
            self.get_stock_price_location = base_config_location
        elseif awful.util.file_readable(sub_module_location .. "/get_stock_price.py") then
            self.get_stock_price_location = sub_module_location
        else
            error("could not find get_stock_price.py")
        end
    end

    self.timer = timer({ timeout = args.timeout or 60 })
    self.timer:connect_signal("timeout", function() self:update() end)
    self.timer:start()
    self:update()

    return self
end

function stock_widget:get_stock_info()
    local f = assert(io.popen(self.get_stock_price_location .. "/get_stock_price.py" .. " " .. self.symbol, "r"))
    local stock_info = assert(f:read("*a"))
    f:close()  -- TODO: it would be nice if I could check the exit code here

    -- split output on space
    local items = {}
    for item in stock_info:gmatch("%S+") do table.insert(items, item) end

    return {
        price  = items[1],
        change = items[2]
    }
end

function stock_widget:update()
    local data = self:get_stock_info()
    if data.price == nil or data.change == nil then
        naughty.notify({
                text = "Error getting stock info for " .. self.symbol
            })
        self.timer:stop()
        return
    end
    data.symbol = self.symbol

    -- colors
    data.symbol_color_on, data.symbol_color_off = color_tags(self.symbol_color)
    data.price_color_on, data.price_color_off = color_tags(self.price_color)

    local change_color = self.gain_color
    if data.change:sub(1,1) == "-" then
        change_color = self.loss_color
    end
    data.change_color_on, data.change_color_off = color_tags(change_color)

    self.widget:set_markup(substitute(self.text_format, data))
end

return setmetatable(stock_widget, {__call = stock_widget.new})
