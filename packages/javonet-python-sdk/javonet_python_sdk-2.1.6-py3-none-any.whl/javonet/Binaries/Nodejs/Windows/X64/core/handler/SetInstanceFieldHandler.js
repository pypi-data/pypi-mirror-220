const AbstractHandler = require("./AbstractHandler");

class SetInstanceFieldHandler extends AbstractHandler {
    constructor() {
        super()
    }

    process(command) {
        try {
            const {payload} = command
            let instance = payload[0]
            let field = payload[1]
            let value = payload[2]

            instance[field] = value
            return 0
        } catch (error) {
            return this.process_stack_trace(error, this.constructor.name)
        }
    }
}

module.exports = new SetInstanceFieldHandler()